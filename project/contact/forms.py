from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                
        }
        ), 
        )

    class Meta:
        model = models.Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category',
        )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            raise ValidationError(
                'Não digite ABC neste campo.',
                code='invalid'
            )

        return first_name



class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        help_text='Use the same password as before.',
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        queryset = User.objects.filter(email=email)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                'Já existe este e-mail.',
                code='invalid'
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            password_validation.validate_password(password1)

        return password1

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('As senhas não batem.')
                )

        return cleaned_data




class RegisterForm(UserCreationForm, UserForm):

    password1 = forms.CharField(
        label='Password',
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ),
        help_text='Use the same password as before.',
    )

    class Meta(UserForm.Meta):
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )




class RegisterUpdateForm(UserForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user