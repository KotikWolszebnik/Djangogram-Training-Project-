from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from django.core.mail import send_mail
from django.http import (HttpResponseForbidden, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now

from .forms import BioChangeForm, LoginForm, PostForm, RegistrationForm
from .models import Account, Following, Like, Picture, Post
from .utils import TokenGenerator, confirm_required, post_method_required

# Create your views here.


def auth_need(request):
    return HttpResponseForbidden(
        content=b'You must be authenticated for doing this',
        )


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            account = form.save()
            send_mail(
                subject='Confirm registration',
                message='',
                from_email='nutmegraw@yandex.ru',
                recipient_list=[account.email],
                html_message=render_to_string(
                    'confirmation_message.html',
                    context=dict(
                        host=request.get_host(),
                        account=account,
                        unique_string=TokenGenerator.make_token(account),
                        ),
                    ),
                )
            login(request, account)
            success(request, "You've got registrate success.")
            return redirect(f'/wall/{account.slug}/')
        error(request, 'Validation failed!')
    return render(request, 'registration.html', dict(form=form))


def login_account(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            account = form.get_user()
            login(request, account)
            return redirect(f'/wall/{account.slug}/')
        error(
            request,
            'The account with this email and / or password doesn´t exist!!',
            )
    return render(request, 'login.html', dict(form=form))


def show_wall(request, account_slug: int, one_post=None):
    if not Account.objects.filter(slug=account_slug).exists():
        return HttpResponseNotFound(content=b'Account with this slug not found') 
    account = Account.objects.get(slug=account_slug)
    data = dict(account=account)
    if request.user.is_authenticated:
        liked_posts = list()
        for post in account.posts.all():
            if request.user in [like.author for like in post.likes.all()]:
                liked_posts.append(post)
        data['liked_posts'] = liked_posts
        if request.user == account:
            data['post_form'] = PostForm()
        if Following.objects.filter(author=request.user, addressee=account)\
                .exists():
            data['subscribed'] = True
        if request.method == 'POST':
            if request.POST.get('edit_bio'):
                data['bio_form'] = BioChangeForm(instance=request.user)
            elif request.POST.get('edit_post_slug'):
                data['edit_post_slug'] = request.POST.get('edit_post_slug')
        if one_post:
            data['post'] = one_post
            data['by_link'] = True
    return render(request, 'wall.html', data)


@confirm_required
@login_required
def get_post_by_slug(request, post_slug: str):
    if not Post.objects.filter(slug=post_slug).exists():
        return HttpResponseNotFound(content=b'Post with this slug not found')
    post = Post.objects.get(slug=post_slug)
    return show_wall(request, post.author.slug, one_post=post)


@login_required
def confirm_registration(request, unique_string: str):
    if not TokenGenerator.check_token(request.user, unique_string):
        error(request, 'Something went wrong, the confirmation failed!')
    else:
        request.user.reg_confirmed_date = now()
        request.user.save()
        success(request, "You've got confirming success.")
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@post_method_required
def add_post(request):
    form = PostForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save(request)
    else:
        error(
            request,
            'The post is empty, or the attached files number is more then 10')
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@post_method_required
def delete_post(request):
    if not Post.objects.filter(slug=request.POST.get('slug')).exists():
        return HttpResponseNotFound(content=b'Post with this slug not found')
    post = Post.objects.get(slug=request.POST.get('slug'))
    if post.author != request.user:
        return HttpResponseForbidden(
            content=b'You can not delete another users posts',
            )
    post.delete()
    return JsonResponse(dict(code=200))


@login_required
@post_method_required
def logout_account(request):
    logout(request)
    return redirect('login')


@confirm_required
@login_required
@post_method_required
def edit_bio(request):
    form = BioChangeForm(request.POST, instance=request.user)
    if form.is_valid:
        form.save()
    else:
        error(request, 'Validation failed!')
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@post_method_required
def setup_avatar(request):
    picture = Picture(
        picture_itself=request.FILES.get('avatar'), author=request.user,
    )
    picture.save()
    request.user.avatar = picture
    request.user.save()
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@post_method_required
def delete_avatar(request):
    if not request.user.avatar:
        return HttpResponseNotFound(content=b'Avatar absent to delete')
    request.user.avatar.avatar_of = None
    request.user.save()
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@post_method_required
def edit_post(request):
    page = redirect(f'/wall/{request.user.slug}/')
    if not (request.POST.get('text') or request.FILES.getlist('pictures')):
        error(request, 'The post must contain something!')
        return page
    post = Post.objects.get(slug=request.POST.get('post_slug'))
    if post.author != request.user:
        return HttpResponseForbidden(
            content=b'You can not edit another users posts',
            )
    post.text = request.POST.get('text')
    post.edited_time = now()
    post.save()
    for picture in request.FILES.getlist('pictures'):
        Picture(
            picture_itself=picture,
            uploader=request.user,
            post=post,
        ).save()
    return page


@confirm_required
@login_required
@post_method_required
def subscribe(request):
    if not Account.objects.filter(slug=request.POST.get('addressee')).exists():
        return HttpResponseNotFound(content=b'Account with this slug not found')
    account = Account.objects.get(slug=request.POST.get('addressee'))
    if account == request.user:
        return HttpResponseForbidden(content=b'You can not subscribe to yourself')
    elif Following.objects.filter(author=request.user, addressee=account)\
            .exists():
        return HttpResponseForbidden(content=b'You are allready subscribed')
    Following(author=request.user, addressee=account).save()
    return JsonResponse(dict(code=200))


@confirm_required
@login_required
@post_method_required
def unsubscribe(request):
    if not Account.objects.filter(slug=request.POST.get('addressee')).exists():
        return HttpResponseNotFound(content=b'Account with this slug not found')
    account = Account.objects.get(slug=request.POST.get('addressee'))
    if account == request.user:
        return HttpResponseForbidden(
            content=b'You can not unsubscribe from yourself',
        )
    elif not Following.objects.filter(author=request.user, addressee=account)\
            .exists():
        return HttpResponseForbidden(
            content=b'You are not subscribed for unsubscribing',
        )
    Following.objects.get(author=request.user, addressee=account).delete()
    return JsonResponse(dict(code=200))


@confirm_required
@login_required
@post_method_required
def like_post(request):
    if not Post.objects.filter(slug=request.POST.get('slug')).exists():
        return HttpResponseNotFound(content=b'Post with this slug not found')
    post = Post.objects.get(slug=request.POST.get('slug'))
    if Like.objects.filter(author=request.user, post=post).exists():
        return HttpResponseForbidden(
            content=b'The post is allready liked by you',
        )
    Like(author=request.user, post=post).save()
    return JsonResponse(dict(likes_number=len(post.likes.all()), code=200))


@confirm_required
@login_required
@post_method_required
def unlike_post(request):
    if not Post.objects.filter(slug=request.POST.get('slug')).exists():
        return HttpResponseNotFound(content=b'Post with this slug not found')
    post = Post.objects.get(slug=request.POST.get('slug'))
    if not Like.objects.filter(author=request.user, post=post).exists():
        return HttpResponseForbidden(
            content=b'The Post is not liked by you to unlike',
        )
    Like.objects.get(author=request.user, post=post).delete()
    return JsonResponse(dict(likes_number=len(post.likes.all()), code=200))
