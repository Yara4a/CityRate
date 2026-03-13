from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from .forms import PostForm
=======
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import PostForm, CustomUserCreationForm
>>>>>>> origin/Rabindra
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
        return redirect("account_page")

    return render(request, "city/create_post.html", {"form": form})


def review_list(request):
    search_query = request.GET.get("q", "").strip()

    reviews = Post.objects.select_related("city", "user").order_by("-created_at")

    if search_query:
        reviews = reviews.filter(city__city_name__icontains=search_query)

    return render(
        request,
        "city/review_list.html",
        {
            "reviews": reviews,
            "search_query": search_query,
        },
    )

@login_required(login_url="login")
def account_page(request):
    search_query = request.GET.get("q", "").strip()

    reviews = Post.objects.select_related("city", "user").filter(
        user=request.user
    ).order_by("-created_at")

    if search_query:
        reviews = reviews.filter(city__city_name__icontains=search_query)

    return render(
        request,
        "city/account_page.html",
        {
            "reviews": reviews,
            "search_query": search_query,
        },
    )

@login_required(login_url="login")
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    form = PostForm(request.POST or None, instance=post)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("account_page")

    return render(request, "city/edit_post.html", {"form": form})


@login_required(login_url="login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("account_page")

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
<<<<<<< HEAD
    return render(request, "city/signup.html")

=======
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
>>>>>>> origin/Rabindra
