from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from .models import Account
from .forms import LoginForm, RegistrationForm

# Create your views here.


@csrf_protect
def login_account(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            account = form.get_user()
            login(request, account)
            return redirect(f'wall/{account.pk}/')
    return render(request, 'login.html', dict(form=form))


@csrf_protect
def logout_account(request):
    logout(request)
    return redirect('login')


@csrf_protect
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            account = form.get_user()
            return redirect(f'wall/{account.pk}/')
    return render(request, 'registration.html', dict(form=form))


def confirm_registration():
    pass


def show_wall(request, account_id: int):
    account = Account.objects.get(pk=account_id)
    
    return render(request, 'wall.html', dict(account=account))
