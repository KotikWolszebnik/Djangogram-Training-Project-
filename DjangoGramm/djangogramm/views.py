from random import choices
from string import ascii_lowercase, digits

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, RegistrationForm
from .models import Account, Picture, Post

# Create your views here.


@csrf_protect
def register(request):
    if request.user.is_authenticated:
        logout(request)
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            account = form.save()
            login(request, account)
            unique_string = ''.join(choices(ascii_lowercase + digits, k=16))
            account.confirmation_token = unique_string
            account.save()
            send_mail(
                subject='Confirm registration',
                message='',
                from_email='nutmegraw@yandex.ru',
                recipient_list=[account.email],
                html_message=render_to_string(
                    'confirmation_message.html',
                    context=dict(
                        account=account,
                        unique_string=unique_string,
                        ),
                    ),
                )
            return redirect(f'/wall/{account.pk}/')
    return render(request, 'registration.html', dict(form=form))


@csrf_protect
def login_account(request):
    if request.user.is_authenticated:
        logout(request)
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            account = form.get_user()
            login(request, account)
            return redirect(f'/wall/{account.pk}/')
    return render(request, 'login.html', dict(form=form))


@csrf_protect
def show_wall(request, account_id: int):
    account = Account.objects.get(pk=account_id)
    data = dict(account=account)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('edit_profile'):
                data['edit_profile'] = True
            elif request.POST.get('edit_post_id'):
                data['edit_post_id'] = int(request.POST.get('edit_post_id'))
    return render(request, 'wall.html', data)


@csrf_protect
def post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('text') or request.FILES.getlist('pictures'):
                post = Post.objects.create(
                    id=None,
                    author=request.user,
                    text=request.POST.get('text'),
                )
                post.save()
                for picture in request.FILES.getlist('pictures'):
                    Picture(
                        picture_itself=picture,
                        uploader=request.user,
                        post=post,
                    ).save()
                return redirect(f'/wall/{request.user.pk}/')
        return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def delete_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Post.objects.get(pk=request.POST.get('id')).delete()
            return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def logout_account(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')


def confirm_registration(request, unique_string: str):
    if request.user.is_authenticated:
        if request.user.confirmation_token == unique_string:
            request.user.reg_confirmed_date = now()
            request.user.save()
            return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.about_yourself = request.POST.get('about_yourself')
            request.user.save()
            return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def setup_avatar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                picture = Picture.objects.get(avatar_of=request.user)
                picture.avatar_of = None
                picture.save()
            except ObjectDoesNotExist:
                pass
            finally:
                Picture(
                    picture_itself=request.FILES.get('avatar'),
                    uploader=request.user,
                    avatar_of=request.user,
                ).save()
                return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def delete_avatar(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                picture = Picture.objects.get(avatar_of=request.user)
                picture.avatar_of = None
                picture.save()
            except ObjectDoesNotExist:
                pass
            finally:
                return redirect(f'/wall/{request.user.pk}/')


@csrf_protect
def edit_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('text') or request.FILES.getlist('pictures'):
                post = Post.objects.get(pk=int(request.POST.get('post_id')))
                post.text = request.POST.get('text')
                post.edited_time = now()
                post.save()
                for picture in request.FILES.getlist('pictures'):
                    Picture(
                        picture_itself=picture,
                        uploader=request.user,
                        post=post,
                    ).save()
                return redirect(f'/wall/{request.user.pk}/')
        return redirect(f'/wall/{request.user.pk}/')
