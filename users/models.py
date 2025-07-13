from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=50, verbose_name="Телефон", help_text="Введите номер телефона"
    )
    city = models.CharField(max_length=50, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


PAYMENT_METHODS = (("cash", "Наличные"), ("transfer", "Перевод на счёт"))


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(
        default=datetime.now, verbose_name="Дата платежа"
    )
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Отдельно оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default="cash",
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платёж {self.user.email}, {self.payment_date}"
