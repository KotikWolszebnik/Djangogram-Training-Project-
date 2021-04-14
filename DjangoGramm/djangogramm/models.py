from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import (CASCADE, SET_NULL, DateTimeField, EmailField,
                              ForeignKey, Model, OneToOneField, SlugField,
                              TextField)

from .utils import make_unique_random_slug

PICTURE_PATH = 'photos/%Y/%m/%d/'
BIO_MAX_LENGHT = 150
POST_MAX_LENGHT = 2200
PICTURE_DESCRIPTION_MAX_LENGHT = 150
COMMENT_MAX_LENGHT = 1000


# Create your models here.


class Account(AbstractUser):
    slug = SlugField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = None
    email = EmailField(unique=True)
    reg_confirmed_date = DateTimeField(auto_now=False, null=True)
    bio = TextField(max_length=BIO_MAX_LENGHT, blank=True, default='')
    avatar = OneToOneField(
        'Picture', on_delete=SET_NULL, blank=True, null=True, related_name='avatar_of')

    def __str__(self):
        return f'< Account : {self.get_full_name()} >'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10, letters=False)
        return super(self.__class__, self).save(*args, **kwargs)


class Post(Model):
    slug = SlugField(unique=True)
    text = TextField(max_length=POST_MAX_LENGHT, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    edited_time = DateTimeField(blank=True, null=True)
    author = ForeignKey(Account, on_delete=CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        txt = 'No text in the Post'
        if self.text:
            txt = self.text[:10]
        return f'< Post : {txt}... >'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10)
        return super(self.__class__, self).save(*args, **kwargs)


class Picture(Model):
    slug = SlugField(unique=True)
    author = ForeignKey(
        Account, on_delete=SET_NULL, null=True, related_name='uploaded_pictures')
    created_at = DateTimeField(auto_now_add=True)
    picture_itself = CloudinaryField('image')
    description = TextField(
        max_length=PICTURE_DESCRIPTION_MAX_LENGHT, blank=True, null=True)
    post = ForeignKey(
        Post, on_delete=SET_NULL, blank=True, null=True, related_name='pictures')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'< Picture : {self.slug} >'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10)
        return super(self.__class__, self).save(*args, **kwargs)


class Comment(Model):
    slug = SlugField(unique=True)
    text = TextField(max_length=COMMENT_MAX_LENGHT)
    created_at = DateTimeField(auto_now_add=True)
    edited_time = DateTimeField(auto_now=True, blank=True, null=True)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        txt = self.text[:10]
        return f'< Comment : {self.author.get_full_name} | {txt}... >'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10)
        return super(self.__class__, self).save(*args, **kwargs)


class Like(Model):
    slug = SlugField(unique=True)
    picture = ForeignKey(Picture, on_delete=CASCADE, blank=True, null=True, related_name='likes')
    post = ForeignKey(Post, on_delete=CASCADE, blank=True, null=True, related_name='likes')
    comment = ForeignKey(Comment, on_delete=CASCADE, blank=True, null=True, related_name='likes')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='likes')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'< Like : {self.author.get_full_name()} | {self.created_at}>'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10)
        return super(self.__class__, self).save(*args, **kwargs)


class Following(Model):
    slug = SlugField(unique=True)
    author = ForeignKey(Account, on_delete=CASCADE, related_name='subscribes')
    addressee = ForeignKey(Account, on_delete=CASCADE, related_name='follows')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'< Following : {self.author.get_full_name()} | {self.addressee.get_full_name}>'

    def save(self, *args, **kwargs):
        make_unique_random_slug(self, 10)
        return super(self.__class__, self).save(*args, **kwargs)
