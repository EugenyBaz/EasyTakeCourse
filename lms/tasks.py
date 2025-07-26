from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import logging


@shared_task
def send_information_about_update_course(emails):
    """Отправляет сообщение подписчику об обновлении курса."""
    logger = logging.getLogger(__name__)
    logger.info(f'Sending notifications to {len(emails)} subscribers.')

    subject = 'Обновление на курсе'
    message = ('Вы получили это письмо так как подписались на обновления.\n'
               'Зайдите в личный кабинет, что бы посмотреть изменения.')
    sender = settings.DEFAULT_FROM_EMAIL

    # Отправляем письма
    send_mail(subject, message, sender, emails, fail_silently=False)





