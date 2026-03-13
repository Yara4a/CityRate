from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_signup_email_required(self):
        # Verify that signing up without an email fails
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password': 'password123',
            'email': '' 
        })
        self.assertEqual(response.status_code, 200) # Form should reload with error
        self.assertFalse(User.objects.filter(username='testuser').exists())