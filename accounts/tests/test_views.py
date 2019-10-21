from django.test import TestCase
from unittest.mock import patch
import accounts.views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def send_login_email_to_test(self):
        return self.client.post('/accounts/send_login_email', data={
            'email': 'test@example.com'
        })
    def test_redirects_to_home_page(self):
        response = self.send_login_email_to_test()
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):

            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        self.send_login_email_to_test()

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['test@example.com'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.send_login_email_to_test()

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['test@example.com'])

    def test_shows_success_message(self):
        response = self.client.post('/accounts/send_login_email',
                                    data={'email': 'test@example.com'},
                                    follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.")
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        self.send_login_email_to_test()
        token = Token.objects.first()
        self.assertEqual(token.email, 'test@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.send_login_email_to_test()
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')
