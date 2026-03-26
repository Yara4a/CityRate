from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a base user to test duplicate email prevention
        self.username = "existinguser"
        self.password = "password123"
        self.email = "test@example.com"
        User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_signup_requires_email(self):
        """Test that a user cannot sign up without an email address."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'password123',
            'email': '' # Empty email
        })
        self.assertEqual(response.status_code, 200) # Should stay on page with errors
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_duplicate_email_prevention(self):
        """Test that the system rejects an email that is already registered."""
        response = self.client.post(reverse('signup'), {
            'username': 'anotheruser',
            'password': 'password123',
            'email': self.email # Same email as 'existinguser'
        })
        self.assertContains(response, "A user with this email already exists.")
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_login_redirect_to_next(self):
        """Test the 'next' parameter redirects users to their intended destination."""
        protected_url = reverse('create_post')
        login_url_with_next = f"{reverse('login')}?next={protected_url}"
        
        response = self.client.post(login_url_with_next, {
            'username': self.username,
            'password': self.password
        })
        # Should redirect to 'create_post', not the homepage
        self.assertRedirects(response, protected_url)