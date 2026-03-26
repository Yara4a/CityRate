from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import pycountry

from .models import Post, City


COUNTRY_NAME_MAP = {
    "Taiwan, Province of China": "Taiwan",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Republic of": "North Korea",
    "Viet Nam": "Vietnam",
    "Russian Federation": "Russia",
    "Iran, Islamic Republic of": "Iran",
    "Syrian Arab Republic": "Syria",
    "Moldova, Republic of": "Moldova",
    "Venezuela, Bolivarian Republic of": "Venezuela",
    "Tanzania, United Republic of": "Tanzania",
    "Bolivia, Plurinational State of": "Bolivia",
    "Palestine, State of": "Palestine",
    "Brunei Darussalam": "Brunei",
    "Lao People's Democratic Republic": "Laos",
    "Myanmar": "Myanmar",
    "Czechia": "Czech Republic",
    "North Macedonia": "Macedonia",
}


def normalize_country_name(country_name):
    return COUNTRY_NAME_MAP.get(country_name, country_name)


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

    country = forms.ChoiceField(
        choices=[("", "Select a country")] + COUNTRY_CHOICES,
        label="Country"
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        required=False,
        empty_label="Select a city",
        label="City"
    )

    city_name = forms.CharField(
        required=False,
        max_length=120,
        label="Or type city manually",
        widget=forms.TextInput(attrs={"placeholder": "Enter city if not listed"})
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
        fields = ["country", "city", "city_name", "review_text", "rating_score"]
        widgets = {
            "review_text": forms.Textarea(attrs={"placeholder": "Share your experience..."})
        }

    def __init__(self, *args, **kwargs):
        selected_country = kwargs.pop("selected_country", None)
        super().__init__(*args, **kwargs)

        country = selected_country or self.data.get("country")

        if not country and self.initial.get("country"):
            country = self.initial.get("country")

        if country:
            normalized_country = normalize_country_name(country)
            self.fields["city"].queryset = City.objects.filter(
                country__iexact=normalized_country
            ).order_by("city_name")
        else:
            self.fields["city"].queryset = City.objects.none()

    def clean_rating_score(self):
        rating = self.cleaned_data.get("rating_score")

        if rating in (None, ""):
            return None

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")

        return rating

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        city_name = (cleaned_data.get("city_name") or "").strip()

        if not city and not city_name:
            raise forms.ValidationError("Please select a city or type one manually.")

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for validation.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email