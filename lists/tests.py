from django.test import TestCase
from django.template.loader import render_to_string

class HomePageTest(TestCase):
    

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)
