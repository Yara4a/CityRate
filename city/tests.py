from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import PostForm
from .models import City, Post


class CityRateTests(TestCase):
    def setUp(self):
        self.password = "StrongPass123!"

        self.user1 = User.objects.create_user(
            username="sable",
            email="sable@example.com",
            password=self.password
        )
        self.user2 = User.objects.create_user(
            username="yara",
            email="yara@example.com",
            password=self.password
        )

        self.city_paris = City.objects.create(city_name="Paris", country="France")
        self.city_tokyo = City.objects.create(city_name="Tokyo", country="Japan")
        self.city_glasgow = City.objects.create(city_name="Glasgow", country="United Kingdom")

        self.public_post_user1 = Post.objects.create(
            user=self.user1,
            city=self.city_paris,
            review_text="Lovely city with great food.",
            rating_score=5,
            is_draft=False,
        )

        self.public_post_user2 = Post.objects.create(
            user=self.user2,
            city=self.city_tokyo,
            review_text="Busy but amazing.",
            rating_score=4,
            is_draft=False,
        )

        self.glasgow_post = Post.objects.create(
            user=self.user1,
            city=self.city_glasgow,
            review_text="Love the West End!",
            rating_score=5,
            is_draft=False,
        )

        self.draft_user1 = Post.objects.create(
            user=self.user1,
            city=self.city_paris,
            review_text="Private draft by user1",
            rating_score=3,
            is_draft=True,
        )

        self.draft_user2 = Post.objects.create(
            user=self.user2,
            city=self.city_tokyo,
            review_text="Private draft by user2",
            rating_score=2,
            is_draft=True,
        )

    # Authentication / signup
    def test_signup_with_email_creates_user(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "VeryStrongPass123!",
            "password2": "VeryStrongPass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_signup_enforces_email(self):
        response = self.client.post(reverse("signup"), {
            "username": "missingemailuser",
            "email": "",
            "password1": "password123ABC!",
            "password2": "password123ABC!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="missingemailuser").exists())

    def test_signup_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("signup"), {
            "username": "anotheruser",
            "email": "sable@example.com",
            "password1": "AnotherStrong123!",
            "password2": "AnotherStrong123!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="anotheruser").exists())
        self.assertContains(response, "A user with this email already exists.")

    # Form / model validation
    def test_invalid_rating_rejected_in_form(self):
        form_data = {
            "country": "United Kingdom",
            "city": self.city_glasgow.id,
            "city_name": "",
            "review_text": "Nice",
            "rating_score": 6,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("rating_score", form.errors)

    def test_create_post_rejects_invalid_rating(self):
        self.client.login(username="sable", password=self.password)

        response = self.client.post(reverse("create_post"), {
            "country": "Spain",
            "city_name": "Madrid",
            "review_text": "Nice place",
            "rating_score": 6,
            "action": "post",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Post.objects.filter(
                user=self.user1,
                city__city_name="Madrid",
                review_text="Nice place"
            ).exists()
        )

    # Permissions / security
    def test_guest_redirect_to_login(self):
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_user_cannot_edit_another_users_post(self):
        self.client.login(username="sable", password=self.password)

        response = self.client.get(
            reverse("edit_post", args=[self.public_post_user2.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_another_users_post(self):
        self.client.login(username="sable", password=self.password)

        response = self.client.post(
            reverse("delete_post", args=[self.public_post_user2.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Post.objects.filter(id=self.public_post_user2.id).exists())

    # Search / filtering / visibility
    def test_search_query_filtering(self):
        response = self.client.get(reverse("review_list"), {"city": "Glasgow"})
        self.assertContains(response, "Love the West End!")

        response_empty = self.client.get(reverse("review_list"), {"city": "London"})
        self.assertNotContains(response_empty, "Love the West End!")

    def test_review_search_returns_matching_published_posts_only(self):
        response = self.client.get(reverse("review_list"), {"q": "Paris"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paris")
        self.assertNotContains(response, "Tokyo")

        reviews = response.context["reviews"]
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews.first().city.city_name, "Paris")
        self.assertFalse(reviews.first().is_draft)

    def test_draft_visibility(self):
        Post.objects.create(
            user=self.user1,
            city=self.city_glasgow,
            review_text="Draft",
            is_draft=True,
            rating_score=4
        )
        response = self.client.get(reverse("review_list"))
        self.assertNotContains(response, "Draft")

    def test_account_page_shows_only_logged_in_users_drafts(self):
        self.client.login(username="sable", password=self.password)

        response = self.client.get(reverse("account_page"), {"tab": "draft"})

        self.assertEqual(response.status_code, 200)

        drafts = response.context["drafts"]
        self.assertEqual(drafts.count(), 1)
        self.assertEqual(drafts.first().user, self.user1)
        self.assertEqual(drafts.first().review_text, "Private draft by user1")

        draft_ids = list(drafts.values_list("id", flat=True))
        self.assertIn(self.draft_user1.id, draft_ids)
        self.assertNotIn(self.draft_user2.id, draft_ids)