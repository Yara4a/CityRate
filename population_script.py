import os
import django
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityRate.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from city.models import City, Post


def random_past_datetime():
    now = timezone.now()
    days_ago = random.randint(0, 180)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    return now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)


def weighted_city_choice(cities, popular_names):
    weighted = []
    for city in cities:
        if city.city_name in popular_names:
            weighted.extend([city] * 4)
        else:
            weighted.extend([city] * 1)
    return random.choice(weighted)


def build_review(city_name, rating):
    openers = [
        f"I recently visited {city_name} and had a really enjoyable time.",
        f"My trip to {city_name} was better than I expected.",
        f"{city_name} ended up being one of the more memorable stops on my trip.",
        f"I spent a few days in {city_name} and came away with mixed but mostly positive feelings.",
        f"{city_name} has a really distinct atmosphere compared with other cities I have visited.",
    ]

    positives = [
        "The food scene was excellent and there were loads of places to explore.",
        "Public transport was easy to use and getting around felt quite convenient.",
        "The city centre was walkable and there were plenty of nice cafés and local shops.",
        "I loved the architecture and there were lots of areas that felt full of character.",
        "There was always something to do, whether it was sightseeing, eating, or just wandering around.",
        "The overall atmosphere felt lively without being too overwhelming.",
        "I found a lot of hidden spots away from the busiest tourist areas.",
    ]

    neutrals = [
        "Some attractions were quite crowded, especially later in the day.",
        "Prices in the central areas were a bit high, but not completely unreasonable.",
        "A few places felt slightly overrated, though the city overall was still worth visiting.",
        "The weather could have been better, but it did not ruin the trip.",
        "It was busier than I expected, especially around the main tourist spots.",
    ]

    negatives = [
        "A few parts felt overpriced and a bit too tourist-focused.",
        "Transport was not always as smooth as I hoped during peak hours.",
        "Some attractions did not quite live up to the hype.",
        "It was harder than expected to avoid the busiest areas.",
        "I probably would not stay too long on a return visit.",
    ]

    closers_good = [
        "I would definitely recommend it for a city break.",
        "I would happily visit again.",
        "I can see why so many people like this place.",
        "Overall, I had a really good experience.",
    ]

    closers_mid = [
        "Overall, I still think it was worth visiting.",
        "I enjoyed it, even though it was not perfect.",
        "I would recommend it, but with realistic expectations.",
        "It was a solid trip overall.",
    ]

    parts = [random.choice(openers), random.choice(positives)]

    if rating >= 4:
        if random.random() < 0.45:
            parts.append(random.choice(neutrals))
        parts.append(random.choice(closers_good))
    elif rating == 3:
        parts.append(random.choice(neutrals))
        if random.random() < 0.5:
            parts.append(random.choice(positives))
        parts.append(random.choice(closers_mid))
    else:
        parts.append(random.choice(negatives))
        if random.random() < 0.4:
            parts.append(random.choice(neutrals))
        parts.append("It was still an interesting place to see once.")

    return " ".join(parts)


def populate():
    print("Starting realistic CityRate population...")


    Post.objects.all().delete()
    City.objects.all().delete()
    User.objects.exclude(username="admin").delete()

    users_data = [
        ("sable", "sable@example.com"),
        ("rabindra", "rabindra@example.com"),
        ("abdullah", "abdullah@example.com"),
        ("emilytravels", "emily@example.com"),
        ("jamescitybreak", "james@example.com"),
        ("sofiaroutes", "sofia@example.com"),
        ("urbanroamer", "urbanroamer@example.com"),
        ("weekendwanderer", "wanderer@example.com"),
        ("nomadnotes", "nomad@example.com"),
        ("globetrotter", "globe@example.com"),
        ("cityhopper", "hopper@example.com"),
        ("quietexplorer", "quiet@example.com"),
        ("trainwindow", "trainwindow@example.com"),
        ("mapandmatcha", "mapandmatcha@example.com"),
        ("latenightwalker", "latenightwalker@example.com"),
    ]

    users = []
    for username, email in users_data:
        user = User.objects.create_user(
            username=username,
            email=email,
            password="Testpass123!"
        )
        users.append(user)

    cities_data = [
        ("London", "United Kingdom"),
        ("Manchester", "United Kingdom"),
        ("Edinburgh", "United Kingdom"),
        ("Paris", "France"),
        ("Lyon", "France"),
        ("Rome", "Italy"),
        ("Milan", "Italy"),
        ("Barcelona", "Spain"),
        ("Madrid", "Spain"),
        ("Lisbon", "Portugal"),
        ("Amsterdam", "Netherlands"),
        ("Berlin", "Germany"),
        ("Munich", "Germany"),
        ("Vienna", "Austria"),
        ("Prague", "Czech Republic"),
        ("Budapest", "Hungary"),
        ("Dublin", "Ireland"),
        ("New York", "United States"),
        ("Chicago", "United States"),
        ("Toronto", "Canada"),
        ("Vancouver", "Canada"),
        ("Tokyo", "Japan"),
        ("Kyoto", "Japan"),
        ("Seoul", "South Korea"),
        ("Bangkok", "Thailand"),
        ("Singapore", "Singapore"),
        ("Sydney", "Australia"),
        ("Melbourne", "Australia"),
        ("Dubai", "United Arab Emirates"),
        ("Istanbul", "Turkey"),
    ]

    cities = []
    for city_name, country in cities_data:
        city = City.objects.create(city_name=city_name, country=country)
        cities.append(city)

    popular_names = {
        "London", "Paris", "Rome", "Barcelona", "Amsterdam",
        "New York", "Tokyo", "Seoul", "Singapore", "Dubai"
    }


    weighted_users = []
    for user in users:
        if user.username in {"emilytravels", "cityhopper", "urbanroamer", "sable", "globetrotter"}:
            weighted_users.extend([user] * 4)
        else:
            weighted_users.extend([user] * 2)

    previous_city = None
    previous_user = None

    all_posts = []

    total_posts = 180

    for _ in range(total_posts):

        city = weighted_city_choice(cities, popular_names)
        retry = 0
        while previous_city and city.city_name == previous_city.city_name and retry < 5:
            city = weighted_city_choice(cities, popular_names)
            retry += 1

    
        user = random.choice(weighted_users)
        retry = 0
        while previous_user and user.username == previous_user.username and retry < 5:
            user = random.choice(weighted_users)
            retry += 1

    
        rating = random.choices(
            population=[2, 3, 4, 5],
            weights=[10, 20, 35, 35],
            k=1
        )[0]

        review_text = build_review(city.city_name, rating)

        post = Post.objects.create(
            user=user,
            city=city,
            review_text=review_text,
            rating_score=rating
        )

        fake_time = random_past_datetime()
        post.created_at = fake_time
        post.save(update_fields=["created_at"])

        all_posts.append(post)
        previous_city = city
        previous_user = user

    print(f"Created {len(users)} users")
    print(f"Created {len(cities)} cities")
    print(f"Created {len(all_posts)} posts")
    print("Done.")
    

if __name__ == "__main__":
    populate()