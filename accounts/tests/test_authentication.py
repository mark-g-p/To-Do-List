from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from unittest import skip
User = get_user_model()


class AuthenticateTest(TestCase):

    def test_returns_None_if_no_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            None,
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_a_new_user_with_correct_email_if_token_exists(self):
        email = 'test@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_an_existing_user_with_correct_email_if_token_exists(self):
        email = 'test@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(None, token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='2test@example.com')
        desired_user = User.objects.create(email='test@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'test@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('test@example.com')
        )
