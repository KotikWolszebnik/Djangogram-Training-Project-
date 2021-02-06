from django.contrib.auth.models import User
from django.db.models import (CASCADE, DO_NOTHING, DateTimeField, ForeignKey,
                              ImageField, Model, TextField)

PICTURE_PATH = 'photos/%Y/%m/%d/'


# Create your models here.


class Account(User):
    username = None
    reg_confirmed_date = DateTimeField(auto_now_add=True)
    about_yourself = TextField(blank=True)
    avatar = ImageField(upload_to=PICTURE_PATH, blank=True)

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
    author = ForeignKey(Account, on_delete=DO_NOTHING)

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
    loading_time = DateTimeField(auto_now_add=True)
    picture_itself = ImageField(upload_to=PICTURE_PATH)
    description = TextField(blank=True)
    picture_preview = ImageField(upload_to=PICTURE_PATH)
    post = ForeignKey(Post, on_delete=DO_NOTHING)

    def like_unlike():
        pass


class Comment(Model):
    text = TextField()
    posted_time = DateTimeField(auto_now_add=True)
    edited_time = DateTimeField(auto_now=True, blank=True)
    post = ForeignKey(Post, on_delete=CASCADE)
    author = ForeignKey(Account, on_delete=DO_NOTHING)

    def __str__(self):
        return f'{self.author}, {self.text}, {self.posted_time}'

    def like_unlike():
        pass


class Like(Model):
    picture = ForeignKey(Picture, on_delete=CASCADE, blank=True)
    post = ForeignKey(Post, on_delete=CASCADE, blank=True)
    comment = ForeignKey(Comment, on_delete=CASCADE, blank=True)
    author = ForeignKey(Account, on_delete=DO_NOTHING)
    time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}, {self.time}'
