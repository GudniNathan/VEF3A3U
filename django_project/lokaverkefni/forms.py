# coding=utf-8
from django import forms
from django.core.validators import RegexValidator

validatorUser = RegexValidator('^[0-9]{10}$', message="Kennitala, án bandstriks")
validatorPass = RegexValidator('^[a-zA-Z][a-zA-Z0-9-_\.]{4,255}$', message="Password should be a combination of letters and numbers")

class LoginForm(forms.Form):
    login_username = forms.CharField(validators=[validatorUser])
    login_password = forms.CharField(validators=[validatorPass])


class KennitalaField(forms.CharField)