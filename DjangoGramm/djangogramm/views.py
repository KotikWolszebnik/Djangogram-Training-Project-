from django.shortcuts import render

# Create your views here.


def show_login_page(request):
    return render(request, 'login.html')


def login():
    pass


def show_registration_page(request):
    return render(request, 'registration.html')


def regisrate():
    pass


def confirm_registration():
    pass


def show_wall(request):
    return render(request, 'wall.html')
