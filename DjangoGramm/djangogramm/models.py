from random import randint

from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, SET_NULL, DateTimeField, EmailField,
                              ForeignKey, ImageField, IntegerField, Model,
                              OneToOneField, TextField)

PICTURE_PATH = 'photos/%Y/%m/%d/'


# Create your models here.


class Account(AbstractUser):
    id = IntegerField(primary_key=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField(unique=True)
    reg_confirmed_date = DateTimeField(auto_now=False, null=True)
    about_yourself = TextField(max_length=150, blank=True)
    confirmation_token = TextField(blank=True, null=True)

    def __str__(self):
        return f'< Account : {self.get_full_name()} >'

    def save(self, *args, **kwargs):
        if not self.id:
            is_unique = False
            while not is_unique:
                id = randint(0, int('9'*10))  # 10 digits
                is_unique = (Account.objects.filter(id=id).count() == 0)
            self.id = id
        super(Account, self).save(*args, **kwargs)


class Post(Model):
    id = IntegerField(primary_key=True, unique=True)
    text = TextField(max_length=2200, blank=True)
    posted_time = DateTimeField(auto_now_add=True, editable=False)
    edited_time = DateTimeField(blank=True, null=True)
    author = ForeignKey(Account, on_delete=CASCADE, related_name='posts')

    class Meta:
        ordering = ['-posted_time']

    def __str__(self):
        txt = 'No text in the Post'
        if self.text:
            txt = self.text[:10]
        return f'< Post : {txt}... >'

    def save(self, *args, **kwargs):
        if not self.id:
            is_unique = False
            while not is_unique:
                id = randint(0, int('9'*10))  # 10 digits
                is_unique = (Post.objects.filter(id=id).count() == 0)
            self.id = id
        super(Post, self).save(*args, **kwargs)


class Picture(Model):
    id = IntegerField(primary_key=True, unique=True)
    uploader = ForeignKey(
        Account, on_delete=SET_NULL, null=True, related_name='uploaded_pictures')
    loading_time = DateTimeField(auto_now_add=True)
    picture_itself = ImageField(upload_to=PICTURE_PATH)
    description = TextField(max_length=150, blank=True)
    post = ForeignKey(
        Post, on_delete=SET_NULL, blank=True, null=True, related_name='pictures')
    avatar_of = OneToOneField(
        Account, on_delete=SET_NULL, blank=True, null=True, related_name='avatar')

    class Meta:
        ordering = ['-loading_time']

    def __str__(self):
        return f'< Picture : {self.id} >'

    def save(self, *args, **kwargs):
        if not self.id:
            is_unique = False
            while not is_unique:
                id = randint(0, int('9'*10))  # 10 digits
                is_unique = (Picture.objects.filter(id=id).count() == 0)
            self.id = id
        super(Picture, self).save(*args, **kwargs)


class Comment(Model):
    id = IntegerField(primary_key=True, unique=True)
    text = TextField(max_length=1000)
    posted_time = DateTimeField(auto_now_add=True)
    edited_time = DateTimeField(auto_now=True, blank=True, null=True)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='comments')

    class Meta:
        ordering = ['posted_time']

    def __str__(self):
        txt = self.text[:10]
        return f'< Comment : {self.author.get_full_name} | {txt}... >'

    def save(self, *args, **kwargs):
        if not self.id:
            is_unique = False
            while not is_unique:
                id = randint(0, int('9'*10))  # 10 digits
                is_unique = (Comment.objects.filter(id=id).count() == 0)
            self.id = id
        super(Comment, self).save(*args, **kwargs)


class Like(Model):
    id = IntegerField(primary_key=True, unique=True)
    picture = ForeignKey(Picture, on_delete=CASCADE, blank=True, related_name='likes')
    post = ForeignKey(Post, on_delete=CASCADE, blank=True, related_name='likes')
    comment = ForeignKey(Comment, on_delete=CASCADE, blank=True, related_name='likes')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='likes')
    time = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f'< Like : {self.author.get_full_name()} | {self.time}>'

    def save(self, *args, **kwargs):
        if not self.id:
            is_unique = False
            while not is_unique:
                id = randint(0, int('9'*10))  # 10 digits
                is_unique = (Like.objects.filter(id=id).count() == 0)
            self.id = id
        super(Like, self).save(*args, **kwargs)
