from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import logging


@shared_task
def send_information_about_update_course(emails):
    try:
        send_mail(
            'Test Subject',
            'This is a test message.',
            settings.DEFAULT_FROM_EMAIL,
            ['eugeny.bazavod@list.ru'],  # Сюда подставьте реальный email
            fail_silently=False
        )
        print("Ну, круто получил же письмо!")
    except Exception as e:
        print(f"Ошибка доставки письма: {e}")
    """Отправляет сообщение подписчику об обновлении курса."""
    logger = logging.getLogger(__name__)
    logger.info(f'Sending notifications to {len(emails)} subscribers.')

    # Проверяем тип данных перед отправкой
    assert isinstance(emails, list), "The argument must be a list of strings."

    subject = 'Обновление на курсе'
    message = 'Вы получили это письмо так как подписались на обновления'
    sender = settings.DEFAULT_FROM_EMAIL

    # Отправляем письма
    send_mail(subject, message, sender, emails, fail_silently=False)



