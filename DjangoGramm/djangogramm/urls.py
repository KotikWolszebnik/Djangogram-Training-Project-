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

from .views import (add_post, auth_need, confirm_registration, delete_avatar,
                    delete_post, edit_bio, edit_post, get_post_by_slug,
                    like_post, login_account, logout_account, register,
                    setup_avatar, show_wall, subscribe, unlike_post,
                    unsubscribe)

urlpatterns = [
    path('', login_account),
    path('login/', login_account, name='login'),
    path('logout/', logout_account, name='logout'),
    path('registration/', register, name='registration'),
    path('bio/edit/', edit_bio, name='profile'),
    path('wall/<int:account_slug>/', show_wall, name='wall'),
    path('confirm/<str:unique_string>/', confirm_registration, name='confirm'),
    path('post/get/<str:post_slug>/', get_post_by_slug, name='get_post_by_slug'),
    path('post/create/', add_post, name='create_post'),
    path('post/edit/', edit_post, name='edit_post'),
    path('post/delete/', delete_post, name='delete_post'),
    path('avatar/create/', setup_avatar, name='create_avatar'),  # Not tested
    path('avatar/delete/', delete_avatar, name='delete_avatar'),
    path('auth_need/', auth_need, name='auth_need'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('post/like/', like_post, name='like_post'),
    path('post/unlike/', unlike_post, name='unlike_post'),
]
