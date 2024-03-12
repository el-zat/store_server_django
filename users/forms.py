from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input password',
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input firstname',
    }))
    lastname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input lastname',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input username',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input email',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Confirm password',
    }))

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'image', 'username', 'email')
