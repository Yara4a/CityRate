from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import PostForm, CustomUserCreationForm
from .models import Post

# Home and General Views

def home(request):
    """Renders the landing page."""
    return render(request, "city/homepage.html")

def review_list(request):
    """Displays all posts, ordered by the most recent."""
    reviews = Post.objects.select_related("city", "user").order_by("-created_at")
    return render(request, "city/review_list.html", {"reviews": reviews})

# Authentication Views

def signup_view(request):
    """Handles user registration using the custom form with email validation."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after successful signup
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "city/signup.html", {"form": form})

def login_view(request):
    """Handles user login and supports redirection via the 'next' parameter."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if there is a 'next' destination (e.g. from @login_required)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "city/login.html", {"form": form})

def logout_view(request):
    """Logs out the user via POST request for security."""
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

# Post Management Views (Protected)

@login_required(login_url="login")
def create_post(request):
    """Allows authenticated users to create a new city review."""
    form = PostForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect("review_list")

    return render(request, "city/create_post.html", {"form": form})

@login_required(login_url="login")
def edit_post(request, post_id):
    """Allows users to edit only their own posts."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("review_list")

    return render(request, "city/edit_post.html", {"form": form})

@login_required(login_url="login")
def delete_post(request, post_id):
    """Allows users to delete only their own posts via POST."""
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("review_list")

    return render(request, "city/delete_post.html", {"post": post})