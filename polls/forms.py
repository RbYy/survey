from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dynamic_preferences.forms import UserSinglePreferenceForm


class RegistrationForm(forms.Form):

    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(
            attrs=dict(required=True, max_length=30)
        ),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Email address"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class CustomPreferenceForm(UserSinglePreferenceForm):

    def save(self, *args, **kwargs):
        if self.cleaned_data['raw_value'] is not None:
            self.instance.value = self.cleaned_data['raw_value']
        else:
            self.cleaned_data['raw_value'] = self.instance.value
        return super(CustomPreferenceForm, self).save(*args, **kwargs)

    def clean(self):
        print('value', self.instance.value)
        super(CustomPreferenceForm, self).clean()
        if self.instance.pk:
            password = self.cleaned_data.get("raw_value")
            if not password:
                self.cleaned_data['raw_value'] = self.instance.value
                del self._errors['raw_value']
        return self.cleaned_data
