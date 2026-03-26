from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import PostForm, CustomUserCreationForm
from .models import Post, City


def home(request):
    return render(request, "city/homepage.html")


def get_or_create_city(city_name, country):
    city = City.objects.filter(
        city_name__iexact=city_name.strip(),
        country__iexact=country.strip()
    ).first()

    if not city:
        city = City.objects.create(
            city_name=city_name.strip(),
            country=country.strip()
        )

    return city


@login_required(login_url="login")
def create_post(request):
    draft_id = request.POST.get("draft_id") or request.GET.get("draft_id")
    mode = request.GET.get("mode")
    is_draft_mode = mode == "draft"
    existing_draft = None

    if draft_id:
        existing_draft = Post.objects.filter(
            id=draft_id,
            user=request.user,
            is_draft=True
        ).first()

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            city_name = form.cleaned_data["city_name"].strip()
            country = form.cleaned_data["country"].strip()
            review_text = form.cleaned_data["review_text"]
            rating_score = form.cleaned_data["rating_score"]

            action = request.POST.get("action")
            if not action:
                action = "draft" if is_draft_mode else "post"

            city = get_or_create_city(city_name, country)

            post = existing_draft if existing_draft else Post(user=request.user)
            post.city = city
            post.review_text = review_text
            post.rating_score = rating_score
            post.is_draft = action == "draft"
            post.save()

            if action == "draft":
                return redirect(f"{redirect('account_page').url}?tab=draft")

            return redirect("account_page")

    else:
        if existing_draft:
            form = PostForm(initial={
                "city_name": existing_draft.city.city_name,
                "country": existing_draft.city.country,
                "review_text": existing_draft.review_text,
                "rating_score": existing_draft.rating_score,
            })
        else:
            form = PostForm()

    return render(
        request,
        "city/create_post.html",
        {
            "form": form,
            "draft_id": existing_draft.id if existing_draft else "",
            "draft_saved": request.GET.get("draft_saved") == "1",
            "is_draft_mode": is_draft_mode,
        },
    )


@require_POST
@login_required(login_url="login")
def autosave_draft(request):
    city_name = (request.POST.get("city_name") or "").strip()
    country = (request.POST.get("country") or "").strip()
    review_text = (request.POST.get("review_text") or "").strip()
    rating_raw = request.POST.get("rating_score")
    draft_id = request.POST.get("draft_id")

    if not city_name and not review_text and not rating_raw:
        return JsonResponse({"saved": False, "draft_id": draft_id or ""})

    if not city_name:
        city_name = "Untitled City"

    if not country:
        country = "United Kingdom"

    rating_score = None
    if rating_raw:
        try:
            rating_score = int(rating_raw)
        except ValueError:
            rating_score = None

    city = get_or_create_city(city_name, country)

    draft = None
    if draft_id:
        draft = Post.objects.filter(
            id=draft_id,
            user=request.user,
            is_draft=True
        ).first()

    if not draft:
        draft = Post.objects.create(
            user=request.user,
            city=city,
            review_text=review_text,
            rating_score=rating_score,
            is_draft=True,
        )
    else:
        draft.city = city
        draft.review_text = review_text
        draft.rating_score = rating_score
        draft.is_draft = True
        draft.save()

    return JsonResponse({"saved": True, "draft_id": draft.id})


def review_list(request):
    search_query = request.GET.get("q", "").strip()
    city_query = request.GET.get("city", "").strip()

    if city_query:
        search_query = city_query

    reviews = Post.objects.select_related("city", "user").filter(
        is_draft=False
    ).order_by("-created_at")

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
    active_tab = request.GET.get("tab", "account")

    all_reviews = Post.objects.select_related("city", "user").filter(
        user=request.user,
        is_draft=False
    ).order_by("-created_at")

    review_count = all_reviews.count()

    reviews = all_reviews
    if search_query and active_tab == "account":
        reviews = reviews.filter(city__city_name__icontains=search_query)

    drafts = Post.objects.select_related("city", "user").filter(
        user=request.user,
        is_draft=True
    ).order_by("-updated_at", "-created_at")

    if search_query and active_tab == "draft":
        drafts = drafts.filter(city__city_name__icontains=search_query)

    return render(
        request,
        "city/account_page.html",
        {
            "reviews": reviews,
            "drafts": drafts,
            "search_query": search_query,
            "active_tab": active_tab,
            "review_count": review_count,
        },
    )


@login_required(login_url="login")
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            city_name = form.cleaned_data["city_name"].strip()
            country = form.cleaned_data["country"].strip()

            city = get_or_create_city(city_name, country)

            post.city = city
            post.review_text = form.cleaned_data["review_text"]
            post.rating_score = form.cleaned_data["rating_score"]

            action = request.POST.get("action", "update")

            if action == "draft":
                post.is_draft = True
                post.save()
                return redirect(f"{redirect('account_page').url}?tab=draft")

            if action == "publish":
                post.is_draft = False
                post.save()
                return redirect("account_page")

            post.save()
            if post.is_draft:
                return redirect(f"{redirect('account_page').url}?tab=draft")
            return redirect("account_page")
    else:
        form = PostForm(initial={
            "city_name": post.city.city_name,
            "country": post.city.country,
            "review_text": post.review_text,
            "rating_score": post.rating_score,
        })

    return render(
        request,
        "city/edit_post.html",
        {
            "form": form,
            "post": post,
        },
    )


@login_required(login_url="login")
def publish_draft(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user, is_draft=True)

    if request.method == "POST":
        post.is_draft = False
        post.save()
        return redirect("account_page")

    return redirect(f"{redirect('account_page').url}?tab=draft")


@login_required(login_url="login")
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        was_draft = post.is_draft
        post.delete()
        if was_draft:
            return redirect(f"{redirect('account_page').url}?tab=draft")
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
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            print("SIGNUP ERRORS:", form.errors)
            print("POST DATA:", request.POST)
    else:
        form = CustomUserCreationForm()

    return render(request, "city/signup.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")

def about_page(request):
    return render(request, 'city/about.html')

def privacy_page(request):
    return render(request, 'city/privacy.html')