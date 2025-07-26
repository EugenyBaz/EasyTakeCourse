from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task(name="users.tasks.check_inactive_users")
def check_inactive_users():
    """Проверяет активен ли пользователь и деактивирует если не заходил более месяца"""

    deadline_inactive_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=deadline_inactive_date, is_active=True
    )

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Deactivated user: {user.email}")
