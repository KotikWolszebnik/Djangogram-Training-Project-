from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, SET_NULL, DateTimeField, EmailField,
                              ForeignKey, ImageField, Model, OneToOneField,
                              TextField)

PICTURE_PATH = 'photos/%Y/%m/%d/'


# Create your models here.


class Account(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField(unique=True)
    reg_confirmed_date = DateTimeField(auto_now_add=True)
    about_yourself = TextField(blank=True)

    def __str__(self):
        return f'{self.get_full_name()}, {self.EMAIL_FIELD}'

    def confirm_registration():
        pass

    def post():
        pass


class Post(Model):
    text = TextField(blank=True)
    posted_time = DateTimeField(auto_now_add=True)
    edited_time = DateTimeField(auto_now=True, blank=True)
    author = ForeignKey(Account, on_delete=CASCADE, related_name='posts')

    def __str__(self):
        txt = 'No text in the Post'
        if self.text:
            txt = self.text[:10]
        return f'{txt}, {self.posted_time}, {self.author}'

    def like_unlike():
        pass

    def comment():
        pass


class Picture(Model):
    uploader = OneToOneField(
        Account, on_delete=SET_NULL, null=True, related_name='uploaded_pictures')
    loading_time = DateTimeField(auto_now_add=True)
    picture_itself = ImageField(upload_to=PICTURE_PATH)
    description = TextField(blank=True)
    picture_preview = ImageField(upload_to=PICTURE_PATH)
    post = ForeignKey(
        Post, on_delete=SET_NULL, blank=True, null=True, related_name='pictures')
    avatar_of = OneToOneField(
        Account, on_delete=SET_NULL, blank=True, null=True, related_name='avatar')

    def like_unlike():
        pass


class Comment(Model):
    text = TextField()
    posted_time = DateTimeField(auto_now_add=True)
    edited_time = DateTimeField(auto_now=True, blank=True)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author}, {self.text}, {self.posted_time}'

    def like_unlike():
        pass


class Like(Model):
    picture = ForeignKey(Picture, on_delete=CASCADE, blank=True, related_name='likes')
    post = ForeignKey(Post, on_delete=CASCADE, blank=True, related_name='likes')
    comment = ForeignKey(Comment, on_delete=CASCADE, blank=True, related_name='likes')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='likes')
    time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}, {self.time}'
