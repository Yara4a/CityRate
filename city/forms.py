from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["city", "review_text", "rating_score"]

    def clean_rating_score(self):
        rating = self.cleaned_data["rating_score"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")

        return rating