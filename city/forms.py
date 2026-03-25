from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import pycountry


COUNTRY_CHOICES = sorted(
    [(country.name, country.name) for country in pycountry.countries],
    key=lambda x: x[0]
)


class PostForm(forms.ModelForm):
    STAR_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    city_name = forms.CharField(
        max_length=120,
        label="City",
        widget=forms.TextInput(attrs={"placeholder": "Enter city name"})
    )

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        label="Country"
    )

    rating_score = forms.TypedChoiceField(
        choices=STAR_CHOICES,
        coerce=int,
        widget=forms.RadioSelect,
        label="Rating score",
        required=False,
    )

    class Meta:
        model = Post
        fields = ["city_name", "country", "review_text", "rating_score"]

    def clean_rating_score(self):
        rating = self.cleaned_data.get("rating_score")

        if rating in (None, ""):
            return None

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")

        return rating


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for validation.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email