from rest_framework.serializers import ValidationError

ALLOWED_DOMAINS = ["youtube.com"]


def validate_link(value):
    """Проверяем ссылку на наличие домена youtube.com"""

    lower_value = value.lower()
    found_domain = any(domain in lower_value for domain in ALLOWED_DOMAINS)

    if not found_domain:
        raise ValidationError(
            f"Ссылка {value} недопустима. Разрешены только ссылки на YouTube."
        )

    return True
