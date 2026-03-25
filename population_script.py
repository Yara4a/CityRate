import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityRate.settings")
django.setup()

from django.contrib.auth.models import User
from city.models import City, Post


def populate():
    # ===== USERS =====
    users_data = [
        ("alice", "alice@example.com"),
        ("bob", "bob@example.com"),
        ("charlie", "charlie@example.com"),
        ("david", "david@example.com"),
        ("emma", "emma@example.com"),
    ]

    users = []
    for username, email in users_data:
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )
        user.set_password("test1234")
        user.save()
        users.append(user)

    # ===== CITIES =====
    cities_data = [
        ("Paris", "France"),
        ("London", "United Kingdom"),
        ("Tokyo", "Japan"),
        ("Seoul", "South Korea"),
        ("New York", "USA"),
        ("Rome", "Italy"),
        ("Barcelona", "Spain"),
        ("Sydney", "Australia"),
    ]

    cities = []
    for city_name, country in cities_data:
        city, _ = City.objects.get_or_create(
            city_name=city_name,
            country=country
        )
        cities.append(city)

    # ===== PUBLIC POSTS =====
    reviews_data = [
        (0, 0, "Beautiful city with amazing food and architecture.", 5),
        (1, 1, "Busy but full of history. Loved the museums.", 4),
        (2, 2, "Super clean and efficient. Public transport is perfect.", 5),
        (3, 3, "Great nightlife and delicious street food.", 4),
        (4, 4, "Very vibrant city, but quite expensive.", 4),
        (0, 5, "Incredible history everywhere you walk.", 5),
        (1, 6, "Relaxed vibe, lovely streets, and great weather.", 4),
        (2, 7, "Amazing views and friendly people.", 5),
        (3, 0, "Romantic atmosphere and lovely cafés.", 5),
        (4, 2, "A bit crowded but definitely worth visiting.", 4),
    ]

    for user_idx, city_idx, text, rating in reviews_data:
        Post.objects.get_or_create(
            user=users[user_idx],
            city=cities[city_idx],
            review_text=text,
            rating_score=rating,
            is_draft=False,
        )

    # ===== DRAFT POSTS =====
    Post.objects.get_or_create(
        user=users[0],
        city=cities[1],
        review_text="Draft: still writing about London...",
        rating_score=3,
        is_draft=True,
    )

    Post.objects.get_or_create(
        user=users[1],
        city=cities[2],
        review_text="Draft: Tokyo trip notes...",
        rating_score=4,
        is_draft=True,
    )

    print("Demo data populated successfully!")


if __name__ == "__main__":
    populate()