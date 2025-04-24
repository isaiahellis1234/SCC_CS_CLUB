from django import forms

from .models import Comment, Post, Category
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False,
        max_length=100,
        help_text="Leave blank if selecting an existing category.",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category (optional)",
    )

    class Meta:
        model = Post
        fields = ["title", "content", "category", "new_category", "image"]

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if new_category:
            category, created = Category.objects.get_or_create(name=new_category)
            cleaned_data["category"] = category

        return cleaned_data


class CommentForm(forms.ModelForm):  # Ensure this is defined
    class Meta:
        model = Comment
        fields = ["content"]


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
