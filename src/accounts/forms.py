from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.fields import CharField
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput

User = get_user_model()


class UserForm(ModelForm):
    """Форма пользователя"""
    password_check = CharField(label="Подтвердите пароль", max_length=128, widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["display_name"].widget.attrs.update({'class': "form-control"})
        self.fields["about"].widget.attrs.update({'class': "form-control"})
        self.fields["avatar"].widget.attrs.update({'class': "form-control"})
        self.fields["password_check"].widget.attrs.update({'class': "form-control"})

    def clean_password_check(self):
        password = self.cleaned_data.get("password_check")
        if not self.instance.check_password(password):
            raise ValidationError("Неверный пароль")
        return password

    class Meta:
        model = User
        fields = "display_name", "about", "avatar", "password_check"
