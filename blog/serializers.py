from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import *

# a serializer for user model

class ProfileSerial(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "bio", "phone", "photo")


class UserInfoSerial(ModelSerializer):
    profile = ProfileSerial()
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "profile")
        

class RespondSerial(ModelSerializer):
    sender = UserInfoSerial()
    class Meta:
        model = Respond()
        fields = ("id", "text", "sender")


class CommentSerial(ModelSerializer):
    sender = UserInfoSerial()
    respond_set = RespondSerial(many=True)
    class Meta:
        model = Comment
        fields = ("id", "text", "sender", "respond_set", "post")


# a serializer for posts
class PostSerial(ModelSerializer):
    author = UserInfoSerial()
    likes = UserInfoSerial(many=True)
    comment_set = CommentSerial(many=True)

    def validate(self, attrs):
        for x in attrs: print(x)
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = ("id", "bodyText", "headline", "author", "comment_set", "comments_count", "likes", "likes_count", "categories", "summery", "pubdate", "moddate")


# a serializer for categories
class CategorySerial(ModelSerializer):
    posts = PostSerial(many=True)
    class Meta:
        model = Category
        fields = ("id", "name", "posts")


# a serializer for WebsiteInfo
class WebsiteInfoSerial(ModelSerializer):
    class Meta:
        model = WebsiteInfo
        exclude = ()


# a serializer for feedbacks
class FeedbackSerial(ModelSerializer):
    class Meta:
        model = Feedback
        exclude = ()
        