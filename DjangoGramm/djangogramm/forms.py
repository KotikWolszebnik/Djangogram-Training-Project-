from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from .models import Account


class LoginForm(AuthenticationForm):
    pass


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Account
        fields = ('email', 'first_name', 'last_name',)


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('about_yourself',)
