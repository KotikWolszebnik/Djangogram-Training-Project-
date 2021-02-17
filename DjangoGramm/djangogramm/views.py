from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
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
                data = dict(account=account, edit_profile=True)
    return render(request, 'wall.html', data)


@csrf_protect
def post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Post(
                id=None,
                author=request.user,
                text=request.POST.get('text'),
            ).save()
            return redirect(f'/wall/{request.user.pk}/')
    return render(request, 'wall.html')


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


def confirm_registration():
    pass


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
        try:
            request.user.avatar.delete()
        except ObjectDoesNotExist:
            pass
        finally:
            if request.method == 'POST':
                Picture(
                    picture_itself=request.FILES.get('avatar'),
                    uploader=request.user,
                    avatar_of=request.user,
                ).save()
                return redirect(f'/wall/{request.user.pk}/')
