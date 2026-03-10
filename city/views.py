from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404



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

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("review_list")

    return render(request, "city/edit_post.html", {"form": form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("review_list")

    return render(request, "city/delete_post.html", {"post": post})