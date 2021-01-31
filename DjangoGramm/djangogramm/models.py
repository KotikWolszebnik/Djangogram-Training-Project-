from django.contrib.auth.models import User
from django.db.models import (CharField, DateTimeField, ForeignKey, Model,
                              TextField)

# Create your models here.


class Account(User):
    reg_confirmed_date = DateTimeField()

    def confirm_registration():
        pass

    def post():
        pass


class Post(Model):
    text = TextField()
    posted_time = DateTimeField()
    edited_time = DateTimeField()
    account = ForeignKey(Account)

    def like_unlike():
        pass

    def comment():
        pass


class Picture(Model):
    picture_itself = CharField()
    preview = CharField()
    post = ForeignKey(Post)


class Comment(Model):
    text = TextField()
    images_refs = CharField()
    posted_time = DateTimeField()
    edited_time = DateTimeField()
    post = ForeignKey(Post)
    author = ForeignKey(Account)

    def like_unlike():
        pass


class Like(Model):
    picture = ForeignKey(Picture)
    post = ForeignKey(Post)
    comment = ForeignKey(Comment)
    author = ForeignKey(Account)
    time = DateTimeField()
