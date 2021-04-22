from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.transaction import atomic
from django.forms import FileInput, ImageField, ModelForm, ValidationError

from .models import Account, Picture, Post


class LoginForm(AuthenticationForm):
    pass


class RegistrationForm(UserCreationForm):
    @atomic
    def save(self, **kwargs):
        account = super(self.__class__, self).save(commit=False, **kwargs)
        account.username = account.email
        account.save()
        return account

    class Meta(UserCreationForm):
        model = Account
        fields = ('email', 'first_name', 'last_name',)


class BioChangeForm(ModelForm):
    class Meta:
        model = Account
        fields = ('bio',)


class PostForm(ModelForm):
    pictures = ImageField(
        required=False,
        widget=FileInput(attrs=dict(multiple='multiple')),
    )

    class Meta:
        model = Post
        fields = ('text',)

    def clean(self):
        if not (self.files.getlist('pictures') or self.data.get('text')):
            raise ValidationError(message=b'Form must contain something')
        elif len(self.files.getlist('pictures')) > 10:
            raise ValidationError(
                message=b'The post images number is limited to 10',
            )
        return self.cleaned_data

    @atomic
    def save(self, request, **kwargs):
        post = super(self.__class__, self).save(commit=False, **kwargs)
        post.author = request.user
        pictures = [Picture(
            picture_itself=picture, author=post.author, post=post,
        ) for picture in self.files.getlist('pictures')]
        post.save()
        for picture in pictures:
            picture.save()
        return post
