from django.contrib import admin

from .models import Account, Comment, Like, Picture, Post

# Register your models here.


for model in [Account, Comment, Like, Picture, Post]:
    admin.site.register(model)
