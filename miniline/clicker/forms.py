from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')

    username = forms.CharField(
        min_length=3,
        max_length=20,
        label='',
        widget=forms.TextInput(attrs={'placeholder': _("Login")}),
    )
    password = forms.CharField(
        min_length=3,
        max_length=20,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': _("Password")}),
    )
    password_confirm = forms.CharField(
        min_length=3,
        max_length=20,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': _("Repeat password")}),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            User.objects.get(username=cleaned_data.get("username"))
        except:
            password = cleaned_data.get("password")
            password_confirm = cleaned_data.get("password_confirm")
            if password != password_confirm:
                raise forms.ValidationError(_("Password not equals!"))
            return cleaned_data
        raise forms.ValidationError(_("User with this login already exist!"))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user
