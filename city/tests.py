from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from city.models import Post, City
from city.forms import PostForm

class CityRateFullCoverageTests(TestCase):
    def setUp(self):
        # Create users for auth and permission testing.
        self.user1 = User.objects.create_user(username="user1", email="u1@test.com", password="password123")
        self.user2 = User.objects.create_user(username="user2", email="u2@test.com", password="password123")
        
        # Create a city and a published post for user1.
        self.city = City.objects.create(city_name="Glasgow", country="United Kingdom")
        self.post1 = Post.objects.create(
            user=self.user1,
            city=self.city,
            review_text="Love the West End!",
            rating_score=5,
            is_draft=False
        )

    # 1. Authentication & registration tests.
    def test_signup_enforces_email(self):
        """Verify that CustomUserCreationForm requires an email."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser', 'password': 'password123', 'email': ''
        })
        self.assertEqual(response.status_code, 200) # Form reloads with error.
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_duplicate_email_rejected(self):
        """Verify the system blocks duplicate email registrations."""
        response = self.client.post(reverse('signup'), {
            'username': 'other', 'password': 'password123', 'email': 'u1@test.com'
        })
        self.assertContains(response, "A user with this email already exists.")

    # 2. Data integrity tests for forms and models.
    def test_invalid_rating_rejected(self):
        """Verify PostForm rejects ratings outside 1-5."""
        form_data = {
            'city_name': 'London', 
            'country': 'United Kingdom', 
            'review_text': 'Nice', 
            'rating_score': 6 # Invalid rating.
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating_score', form.errors)

    # 3. Security and permissions tests.
    def test_ownership_security_on_edit(self):
        """Verify User2 cannot access or edit User1's post."""
        self.client.login(username="user2", password="password123")
        response = self.client.get(reverse('edit_post', args=[self.post1.id]))
        # View uses get_object_or_404(Post, id=post_id, user=request.user).
        self.assertEqual(response.status_code, 404)

    def test_guest_redirect_to_login(self):
        """Verify guests are redirected when trying to access the create page."""
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    # 4. Functional logic tests for views, including search and filtering.
    def test_search_query_filtering(self):
        """Verify the search query correctly filters reviews by city."""
        response = self.client.get(reverse('review_list'), {'city': 'Glasgow'})
        self.assertContains(response, "Glasgow")
        
        response_empty = self.client.get(reverse('review_list'), {'city': 'London'})
        self.assertNotContains(response_empty, "Glasgow")

    def test_draft_visibility(self):
        """Verify that drafts do not appear in the public review list."""
        Post.objects.create(
            user=self.user1, city=self.city, review_text="Draft", is_draft=True
        )
        response = self.client.get(reverse('review_list'))
        self.assertNotContains(response, "Draft")