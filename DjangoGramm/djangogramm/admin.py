from django.contrib import admin

from .models import Account, Comment, Like, Picture, Post

# Register your models here.


admin.site.register(Account, Comment, Like, Picture, Post)
