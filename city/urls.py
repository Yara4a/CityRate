from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("create/autosave/", views.autosave_draft, name="autosave_draft"),
    path("reviews/", views.review_list, name="review_list"),
    path("account/", views.account_page, name="account_page"),
    path("homepage/", views.home, name="home"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("publish/<int:post_id>/", views.publish_draft, name="publish_draft"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]