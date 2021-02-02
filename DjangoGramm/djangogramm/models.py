from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import (CASCADE, DO_NOTHING, DateTimeField, ForeignKey,
                              ImageField, Model, TextField)

PICTURE_PATH = FileSystemStorage(location='/media/photos/')


# Create your models here.


class Account(User):
    reg_confirmed_date = DateTimeField()
    about_yourself = TextField()
    avatar = ImageField(storage=PICTURE_PATH)

    def confirm_registration():
        pass

    def post():
        pass


class Post(Model):
    text = TextField()
    posted_time = DateTimeField()
    edited_time = DateTimeField()
    account = ForeignKey(Account, on_delete=DO_NOTHING)

    def like_unlike():
        pass

    def comment():
        pass


class Picture(Model):
    picture_itself = ImageField(storage=PICTURE_PATH)
    description = TextField()
    picture_preview = ImageField(storage=PICTURE_PATH)
    post = ForeignKey(Post, on_delete=DO_NOTHING)

    def like_unlike():
        pass


class Comment(Model):
    text = TextField()
    posted_time = DateTimeField()
    edited_time = DateTimeField()
    post = ForeignKey(Post, on_delete=CASCADE)
    author = ForeignKey(Account, on_delete=DO_NOTHING)

    def like_unlike():
        pass


class Like(Model):
    picture = ForeignKey(Picture, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    comment = ForeignKey(Comment, on_delete=CASCADE)
    author = ForeignKey(Account, on_delete=DO_NOTHING)
    time = DateTimeField()
