from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError


def validate_email_domain(email):
    try:
        valid = validate_email(email, check_deliverability=True)

        normalized_email = valid.email.lower()
        return normalized_email

    except EmailNotValidError as e:
        raise ValidationError(f"Некорректный email: {str(e)}")
