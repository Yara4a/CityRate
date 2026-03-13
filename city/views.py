from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import PostForm, CustomUserCreationForm
from .models import Post

def home(request):
    return render(request, "city/homepage.html")

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

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "city/login.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signing up
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "city/signup.html", {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home') # Redirect if accessed via GET