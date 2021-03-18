from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, ImageField, FileInput, ValidationError

from .models import Account, Post, Picture


class LoginForm(AuthenticationForm):
    pass


class RegistrationForm(UserCreationForm):
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
        return self.cleaned_data

    def save(self, request, commit=True, **kwargs):
        post = super(self.__class__, self).save(commit=False, **kwargs)
        post.author = request.user
        if commit:
            post.save()
            for picture in self.files.getlist('pictures'):
                picture = Picture(
                    picture_itself=picture,
                    author=post.author,
                    post=post,
                    ).save()
        return post
