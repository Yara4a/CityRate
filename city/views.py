from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import PostForm
from .models import Post


@login_required(login_url="login")
def create_post(request):
    form = PostForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect("review_list")

    return render(request, "city/create_post.html", {"form": form})


def login_page(request):
    return HttpResponse("Login page coming soon.")


def review_list(request):
    reviews = Post.objects.select_related("city", "user").order_by("-created_at")
    return render(request, "city/review_list.html", {"reviews": reviews})


@login_required(login_url="login")
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("review_list")

    return render(request, "city/edit_post.html", {"form": form})


@login_required(login_url="login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("review_list")

    return render(request, "city/delete_post.html", {"post": post})