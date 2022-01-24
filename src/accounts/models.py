from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse

from django_resized import ResizedImageField

from src.base.services import get_avatar_upload_path
from src.accounts.managers import UserManager, FollowerManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("E-mail", max_length=255, validators=[validators.validate_email], unique=True)
    display_name = models.CharField("Отображаемое имя", max_length=100, blank=True)
    about = models.TextField("О пользователе", max_length=2000, blank=True)
    avatar = ResizedImageField(
        "Аватар",
        size=[250, 250],
        crop=['middle', 'center'],
        upload_to=get_avatar_upload_path,
        validators=[validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("account_profile", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return self.email

    def get_short_name(self) -> str:
        if self.display_name:
            return self.display_name
        return self.email


class Follower(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="followers", verbose_name="Пользователь")
    subscriber = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Подписчик")

    objects = FollowerManager()

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f"{self.subscriber} подписался на {self.user}"
