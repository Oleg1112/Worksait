"""
Definition of forms.
"""

from dataclasses import fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment

from django.db import models
from .models import Comment
from .models import Blog
from .models import Course
from .models import Product

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Логин'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Пароль'
        })
    )


class RegistrationForm(UserCreationForm):
    """
    Registration form.
    """
    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
        'username_exists': _("Пользователь с таким именем уже существует."),
        'email_exists': _("Пользователь с таким email уже существует."),
        'password_too_short': _("Пароль слишком короткий."),
        'username_too_short': _("Имя пользователя слишком короткое."),
        'username_too_long': _("Имя пользователя слишком длинное."),
        'email_too_long': _("Email слишком длинный."),
        'password_too_long': _("Пароль слишком длинный."),
        'username_invalid': _("Имя пользователя содержит недопустимые символы."),
        'password_invalid': _("Пароль содержит недопустимые символы."),
        'email_invalid': _("Email содержит недопустимые символы."),
    }
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Логин'
        })
    )
    first_name = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )
    last_name = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Фамилия'
        })
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder':'Email'
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Пароль'
        })
    )
    password2 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Пароль'
        })
    )


class CommentForm (forms.ModelForm):
      class Meta:
         model = Comment
         fields = ('text',)
         labels = {'text': "Комментарий"}

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','descriprion','content', 'image')
        labels = {'title':"Заголовок",'descriprion':"Краткое содержание", 'content':"Полное содержание",'image': "Картинка" }

class CourseForm (forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','content', 'price', 'lessons_count', 'full_course_price', 'start_date', 'fdate_date')

class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','content', 'category', 'price', 'stock', 'image')
        labels = {'title':"Наименование",'content':"Описание", 'category':"Категория", 'price':"Цена", 'stock': "Количество",'image': "Картинка" }

class EnrollCourseForm(forms.Form):
    course_id = forms.IntegerField()
    phone = forms.CharField()
