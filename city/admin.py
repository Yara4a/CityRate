from django.contrib import admin
from .models import City, Post

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_name", "country")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("city", "rating_score", "user", "created_at")
    list_filter = ("rating_score", "city")
    search_fields = ("review_text", "city__city_name", "user__username")
