from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class City(models.Model):
    city_name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.city_name}, {self.country}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="posts")

    review_text = models.TextField(blank=True)
    rating_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
    )

    is_draft = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Draft" if self.is_draft else "Post"
        rating = self.rating_score if self.rating_score is not None else "-"
        return f"{self.city.city_name} - {rating}/5 ({status})"