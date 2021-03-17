from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from django.core.mail import send_mail
from django.http import (HttpResponseForbidden, HttpResponseNotAllowed,
                         HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now
from nanoid import generate

from .forms import BioChangeForm, LoginForm, PostForm, RegistrationForm
from .models import Account, Picture, Post


class TokenGenerator(object):
    tokens_storage = list()

    def __init__(self, account):
        self.token = generate(size=40)
        self.account = account

    @classmethod
    def check_token(cls, account, token: str):
        for token_obj in cls.tokens_storage:
            if token_obj.token == token and token_obj.account == account:
                cls.tokens_storage.remove(token_obj)
                return True
        return False

    @classmethod
    def make_token(cls, account) -> str:
        obj = TokenGenerator(account)
        cls.tokens_storage.append(obj)
        return obj.token


def POST_method_required(func):
    def wrapper(request):
        if request.method == 'POST':
            return func(request)
        return HttpResponseNotAllowed(['POST'])
    return wrapper


def confirm_required(func):
    def wrapper(request):
        if request.user.reg_confirmed_date:
            return func(request)
        return HttpResponseForbidden(
            content=b'You must confirm registration for doing this',
            )
    return wrapper
# Create your views here.


def auth_need(request):
    return HttpResponseForbidden(
        content=b'You must be authenticated for doing this',
        )


def register(request):
    form = RegistrationForm()
    page = render(request, 'registration.html', dict(form=form))
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
            success(request, 'register_success')
            return redirect(f'/wall/{account.slug}/')
        error(request, 'validation_error!')
    return page


def login_account(request):
    form = LoginForm()
    page = render(request, 'login.html', dict(form=form))
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            account = form.get_user()
            login(request, account)
            return redirect(f'/wall/{account.slug}/')
        error(request, 'account_not_exist!')
        return page
    return page


def show_wall(request, account_slug: int):
    if Account.objects.filter(slug=account_slug).exists():
        account = Account.objects.get(slug=account_slug)
        data = dict(account=account, post_form=PostForm())
        if request.user.is_authenticated:
            if request.method == 'POST':
                if request.POST.get('edit_profile'):
                    data['bio_form'] = BioChangeForm(instance=request.user)
                elif request.POST.get('edit_post_slug'):
                    data['edit_post_slug'] = request.POST.get('edit_post_slug')
        return render(request, 'wall.html', data)
    return HttpResponseNotFound


@confirm_required
@login_required
def get_post_by_slug(request, post_slug: str):
    if Post.objects.filter(slug=post_slug).exists():
        post = Post.objects.get(slug=post_slug)
        if post.author == request.user or request.user.reg_confirmed_date():
            return render(
                request, 'wall.html', dict(
                    account=post.author, post=post, by_link=True,
                ),
            )
        error(request, 'not_confirmed!')
        return render(request, 'wall.html', dict(account=post.author))
    return HttpResponseNotFound()


@login_required
def confirm_registration(request, unique_string: str):
    page = redirect(f'/wall/{request.user.slug}/')
    if TokenGenerator.check_token(request.user, unique_string):
        request.user.reg_confirmed_date = now()
        request.user.save()
        success(request, 'confirm_success')
        return page
    error(request, 'confirm_fail!')
    return page


@confirm_required
@POST_method_required
@login_required
def add_post(request):
    page = redirect(f'/wall/{request.user.slug}/')
    form = PostForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save(request)
        return page
    error(request, 'post_is_empty!')
    return page


@confirm_required
@login_required
@POST_method_required
def delete_post(request):
    if Post.objects.filter(slug=request.POST.get('slug')).exists():
        post = Post.objects.get(slug=request.POST.get('slug'))
        if post.author == request.user:
            post.delete()
            return redirect(f'/wall/{request.user.slug}/')
        return HttpResponseForbidden()
    return HttpResponseNotFound()


@login_required
@POST_method_required
def logout_account(request):
    logout(request)
    return redirect('login')


@confirm_required
@login_required
@POST_method_required
def edit_bio(request):
    page = redirect(f'/wall/{request.user.slug}/')
    form = BioChangeForm(request.POST, instance=request.user)
    if form.is_valid:
        form.save()
        return page
    error(request, 'validation_error!')
    return page


@confirm_required
@login_required
@POST_method_required
def setup_avatar(request):
    picture = Picture(
        picture_itself=request.FILES.get('avatar'),
        author=request.user,
    )
    picture.save()
    request.user.avatar = picture
    request.user.save()
    return redirect(f'/wall/{request.user.slug}/')


@confirm_required
@login_required
@POST_method_required
def delete_avatar(request):
    if request.user.avatar:
        request.user.avatar.avatar_of = None
        request.user.save()
        return redirect(f'/wall/{request.user.slug}/')
    return HttpResponseNotFound()


@confirm_required
@login_required
@POST_method_required
def edit_post(request):
    page = redirect(f'/wall/{request.user.slug}/')
    if request.POST.get('text') or request.FILES.getlist('pictures'):
        post = Post.objects.get(slug=request.POST.get('post_slug'))
        if post.author == request.user:
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
        return HttpResponseForbidden()
    error(request, 'post_is_empty!')
    return page
