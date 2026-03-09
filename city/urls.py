from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("reviews/", views.review_list, name="review_list"),
]