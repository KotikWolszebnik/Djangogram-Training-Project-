from string import digits
from nanoid import generate
from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, SET_NULL, DateTimeField, EmailField,
                              ForeignKey, ImageField, Model, OneToOneField,
                              SlugField, TextField)

PICTURE_PATH = 'photos/%Y/%m/%d/'
BIO_MAX_LENGHT = 150
POST_MAX_LENGHT = 2200
PICTURE_DESCRIPTION_MAX_LENGHT = 150
COMMENT_MAX_LENGHT = 1000


def save_with_random_slug(obj, slug_lenght: int, letters=True, *args, **kwargs):
    if not obj.slug:
        is_unique = False
        while not is_unique:
            slug = generate(alphabet=digits, size=slug_lenght)
            if letters:
                slug = generate(size=slug_lenght)
            is_unique = (obj.__class__.objects.filter(slug=slug).count() == 0)
        obj.slug = slug
    super(obj.__class__, obj).save(*args, **kwargs)

# Create your models here.


class Account(AbstractUser):
    slug = SlugField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField(unique=True)
    reg_confirmed_date = DateTimeField(auto_now=False, null=True)
    bio = TextField(max_length=BIO_MAX_LENGHT, blank=True, default='')
    avatar = OneToOneField(
        'Picture', on_delete=SET_NULL, blank=True, null=True, related_name='avatar_of')

    def __str__(self):
        return f'< Account : {self.get_full_name()} >'

    def save(self, *args, **kwargs):
        return save_with_random_slug(self, 10, letters=False, *args, **kwargs)


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
        return save_with_random_slug(self, 10, *args, **kwargs)


class Picture(Model):
    slug = SlugField(unique=True)
    author = ForeignKey(
        Account, on_delete=SET_NULL, null=True, related_name='uploaded_pictures')
    created_at = DateTimeField(auto_now_add=True)
    picture_itself = ImageField(upload_to=PICTURE_PATH)
    description = TextField(
        max_length=PICTURE_DESCRIPTION_MAX_LENGHT, blank=True, null=True)
    post = ForeignKey(
        Post, on_delete=SET_NULL, blank=True, null=True, related_name='pictures')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'< Picture : {self.slug} >'

    def save(self, *args, **kwargs):
        return save_with_random_slug(self, 10, *args, **kwargs)


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
        return save_with_random_slug(self, 10, *args, **kwargs)


class Like(Model):
    slug = SlugField(unique=True)
    picture = ForeignKey(Picture, on_delete=CASCADE, blank=True, related_name='likes')
    post = ForeignKey(Post, on_delete=CASCADE, blank=True, related_name='likes')
    comment = ForeignKey(Comment, on_delete=CASCADE, blank=True, related_name='likes')
    author = ForeignKey(Account, on_delete=CASCADE, related_name='likes')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'< Like : {self.author.get_full_name()} | {self.created_at}>'

    def save(self, *args, **kwargs):
        return save_with_random_slug(self, 10, *args, **kwargs)
