"""DjangoGramm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (edit_profile, login_account, logout_account, post,
                    register, show_wall, delete_post)

urlpatterns = [
    path('', login_account, name='login'),
    path('login/', login_account, name='login'),
    path('logout/', logout_account, name='logout'),
    path('registration/', register, name='registration'),
    path('profile/', edit_profile, name='profile'),
    path('wall/<int:account_id>/', show_wall, name='wall'),
    path('post/', post, name='post'),
    path('post/delete/', delete_post, name='delete_post')
]
