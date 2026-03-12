from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("reviews/", views.review_list, name="review_list"),
    path("account/", views.account_page, name="account_page"),
    path("homepage/", views.home, name="home"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
]