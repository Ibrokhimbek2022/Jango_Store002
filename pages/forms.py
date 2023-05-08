from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "rating": forms.Select(attrs={
                "class": "form-select"
            })
        }
