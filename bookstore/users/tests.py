from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from users.validators import validate_email_domain


class EmailValidatorTests(TestCase):
    @parameterized.expand(
        [
            ("gmail", "user@gmail.com"),
            ("yandex", "user@yandex.ru"),
            ("mailru", "user@mail.ru"),
        ]
    )
    def test_valid_email_passes(self, name, email):
        validate_email_domain(email)

    @parameterized.expand(
        [
            ("no_domain", "user@gmail"),
            ("typo_gmail", "user@yndex.com"),
            ("nonexistent", "user@nonexistentdomain12345.com"),
        ]
    )
    def test_invalid_email_fails(self, name, email):
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_email_normalization(self):
        result = validate_email_domain("USER@GMAIL.COM")
        self.assertEqual(result, "user@gmail.com")
