from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/preview/", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/preview/", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Курс",
    )

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} is subscribed to {self.course.name}"
