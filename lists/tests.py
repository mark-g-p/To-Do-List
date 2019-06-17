from django.test import TestCase

class SmokeTest(TestCase):
    
    def test_bad_maths(self):
        self.assertEqual(1+2,4)
# Create your tests here.
