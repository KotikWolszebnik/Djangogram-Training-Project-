from django.db.models import Model
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Account(AbstractUser):
    pass


class Post(Model):
    pass


class Comment(Model):
    pass


class Like(Model):
    pass
