import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityRate.settings")
django.setup()

from city.models import City


def populate():
    print("Importing cities...")

    # ⚠️ DO NOT delete everything blindly anymore
    # City.objects.all().delete()

    added = set()
    count = 0

    with open("worldcities.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            city_name = (row.get("city") or "").strip()
            country = (row.get("country") or "").strip()
            population = row.get("population")

            if not city_name or not country:
                continue

            # only keep proper cities (no tiny villages)
            if population:
                try:
                    if float(population) < 100000:
                        continue
                except:
                    pass

            key = (city_name.lower(), country.lower())

            if key in added:
                continue

            added.add(key)

            City.objects.get_or_create(
                city_name=city_name,
                country=country
            )

            count += 1

    print(f"Imported {count} cities")


if __name__ == "__main__":
    populate()