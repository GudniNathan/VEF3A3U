# coding=utf-8
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from . import validateKennitala

validatorUser = RegexValidator('^[0-9]{10}$', message="Kennitala, án bandstriks")
validatorPass = RegexValidator('^[a-zA-Z][a-zA-Z0-9-_\.]{4,255}$', message="Password should be a combination of letters and numbers")

class KennitalaField(forms.CharField):
    default_validators = [validatorUser]

    def validate(self, value):
        super(KennitalaField, self).validate(value)

        if not validateKennitala.validate(value):
            raise forms.ValidationError(
                _('%(value)s er ekki kennitala'),
                params={'value': value},
            )

class LoginForm(forms.Form):
    login_username = KennitalaField()
    login_password = forms.CharField(validators=[validatorPass])

class RegisterForm(forms.Form):
    register_username = KennitalaField()
    register_password = forms.CharField(validators=[validatorPass])
    register_password_repeat = forms.CharField(validators=[validatorPass])

    def __init__(self, value):
        super(RegisterForm, self).__init__(value)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        register_password = cleaned_data.get("register_password")
        register_password_repeat = cleaned_data.get("register_password_repeat")

        if register_password and register_password_repeat:
            if register_password != register_password_repeat:
                raise forms.ValidationError(
                    _('Password mismatch.'),
                    code='invalid',
                    params={},
                )

        return cleaned_data