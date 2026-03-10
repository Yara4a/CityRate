from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post

def home(request):
    return render(request, "city/homepage.html")

def create_post(request):
    form = PostForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)

        # Independent mode: attach to a dummy user
        post.user = User.objects.first()

        post.save()
        return redirect("review_list")

    return render(request, "city/create_post.html", {"form": form})


def review_list(request):
    reviews = Post.objects.select_related("city", "user").order_by("-created_at")
    return render(request, "city/review_list.html", {"reviews": reviews})