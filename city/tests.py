from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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

    def test_signup_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("signup"), {
            "username": "anotheruser",
            "email": "sable@example.com",  # already used by user1
            "password1": "AnotherStrong123!",
            "password2": "AnotherStrong123!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="anotheruser").exists())
        self.assertContains(response, "A user with this email already exists.")

    def test_create_post_rejects_invalid_rating(self):
        self.client.login(username="sable", password=self.password)

        response = self.client.post(reverse("create_post"), {
            "city_name": "Madrid",
            "country": "Spain",
            "review_text": "Nice place",
            "rating_score": 6,   # invalid
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

    def test_review_search_returns_matching_published_posts_only(self):
        response = self.client.get(reverse("review_list"), {"q": "Paris"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paris")
        self.assertNotContains(response, "Tokyo")

        reviews = response.context["reviews"]
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews.first().city.city_name, "Paris")
        self.assertFalse(reviews.first().is_draft)

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