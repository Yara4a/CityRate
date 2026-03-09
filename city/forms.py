from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["city", "review_text", "rating_score"]
        widgets = {
            "review_text": forms.Textarea(attrs={"rows": 4}),
        }