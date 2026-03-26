import os
import django
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityRate.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from city.models import City, Post


USERNAMES = [
    "travelgirl23",
    "nomad_jack",
    "citylover",
    "wanderalex",
    "foodie_ella",
    "backpacker_tom",
    "sunset_sam",
    "urban_zoe",
    "weekendmia",
    "roamryan",
]

REVIEW_TEXTS = [
    "Absolutely loved this place, would come back again!",
    "Nice city but a bit too crowded for me.",
    "Food was amazing and people were super friendly.",
    "Not bad, but I expected more honestly.",
    "Such a beautiful place, especially at sunset.",
    "Transport was easy and everything was accessible.",
    "Would recommend for a short trip, not too long.",
    "One of my favourite cities so far!",
    "Really lively atmosphere and lots to explore.",
    "A decent place overall, though a bit expensive in some areas.",
    "Beautiful streets, great cafés, and loads of character.",
    "I enjoyed the trip, but I think two days would have been enough.",
]

GOOD_REVIEW_TEXTS = [
    "I had such a lovely time here. The city felt vibrant, safe, and easy to explore.",
    "This ended up being one of my favourite city breaks. Great atmosphere and brilliant food.",
    "Really enjoyed my stay here. There was loads to do and the city had so much character.",
    "A beautiful place to visit. I would happily recommend it to friends.",
]

MID_REVIEW_TEXTS = [
    "Overall it was a decent trip, though some parts were a bit underwhelming.",
    "I liked it, but I do not think I would stay too long next time.",
    "Worth visiting once, especially for the main attractions.",
    "A solid city break, even if it did not completely wow me.",
]


def random_past_datetime():
    now = timezone.now()
    days_ago = random.randint(0, 180)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    return now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)


def create_demo_users():
    users = []

    for username in USERNAMES:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@example.com"}
        )

        if created:
            user.set_password("password123")
            user.save()

        users.append(user)

    return users


def build_review_text(rating):
    if rating >= 4:
        return random.choice(GOOD_REVIEW_TEXTS)
    if rating == 3:
        return random.choice(MID_REVIEW_TEXTS)
    return random.choice(REVIEW_TEXTS)


def populate():
    print("Creating demo reviews...")

    cities = list(City.objects.all())
    if not cities:
        print("No cities found. Run import_cities.py first.")
        return

    users = create_demo_users()

    created_count = 0

    for _ in range(40):
        user = random.choice(users)
        city = random.choice(cities)
        rating = random.randint(2, 5)

        post = Post.objects.create(
            user=user,
            city=city,
            review_text=build_review_text(rating),
            rating_score=rating,
            is_draft=False,
        )

        fake_time = random_past_datetime()
        post.created_at = fake_time
        post.save(update_fields=["created_at"])

        created_count += 1

    print(f"Created {created_count} demo reviews.")


if __name__ == "__main__":
    populate()