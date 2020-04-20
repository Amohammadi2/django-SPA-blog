from django import forms
from django.contrib.auth.models import User
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            "headline": forms.TextInput({"placeholder": "enter the headline", "class": "form-control"}),
            "bodyText": forms.Textarea({"placeholder": "enter the whole text here", "class": "form-control"}),
            "categories": forms.SelectMultiple({"class": "form-control"}),
            "summery": forms.Textarea({"class": "form-control", "placeholder": "enter the summery of text"}),
        }
        fields = ("headline", "bodyText", "categories", "summery")


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            "password": forms.PasswordInput({"class": "form-control", "placeholder": "enter password"}),
            "username": forms.TextInput({"class": "form-control", "placeholder": "enter your username"}),
        }
        fields = ("username", "password")

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            "password": forms.PasswordInput({"class": "form-control", "placeholder": "enter your password"}),
            "email": forms.EmailInput({"class": "form-control", "placeholder": "enter your email"}),
            "username": forms.TextInput({"class": "form-control", "placeholder": "enter your username"}),
            "first_name": forms.TextInput({"class": "form-control", "placeholder": "enter your first name"}),
            "last_name": forms.TextInput({"class": "form-control", "placeholder": "enter your last name"}),
        }
        fields = ("username", "password", "first_name", "last_name", "email")


# the form that will be displayed to send comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            "text": forms.Textarea({
                "class": "form-control",
                "placeholder": "enter your text",
            })
        }
        fields = ("text",)

# the form that will be displayed to send respond
class RespondForm(forms.ModelForm):
    class Meta:
        model = Respond
        widgets = {
            "text": forms.Textarea({
                "class": "form-control",
                "placeholder": "enter your text",
            })
        }
        fields = ("text",)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        widgets = {
            "text": forms.Textarea({
                "class": "form-control",
                "placeholder": "enter your feedback",
            })
        }
        fields = ("text",)


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            "bio": forms.TextInput(attrs={"placeholder": "enter biography", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "enter your phone number", "class": "form-control"})
        }
        fields = ("bio", "phone")