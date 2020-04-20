from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# a profile for each user to save additional data
class Profile(models.Model):
    bio = models.CharField(max_length=200, default="hi I am a user")
    phone = models.BigIntegerField(blank=True, null=True)
    photo = models.ImageField("image", upload_to="profiles/%Y/%m/", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "'s profile"

class PostManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_by_author(self, usr):
        return self.get_queryset().filter(author=usr)

    def get_newest(self, count:int):
        query = self.get_queryset().order_by("-id")
        if count > len(query):
            return query
        else:
            return query[:count]

    def get_popular(self, count:int):
        query = self.get_queryset().filter(likes_count__gte=20).order_by("-likes_count")
        if count > len(query):
            return query
        else:
            return query[:count]

    def get_controversial(self, count:int):
        query = self.get_queryset().filter(comments_count__gte=10).order_by("-comments_count")
        if count > len(query):
            return query
        else:
            return query[:count]


# categories for posts
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# blog's post
class Post(models.Model):
    headline = models.CharField(max_length=200)
    summery = models.TextField("post's summery", max_length=1000)
    bodyText = models.TextField("post's text", max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = PostManager()
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    likes = models.ManyToManyField(User, related_name="popular_posts", blank=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    pubdate = models.DateField("published date")
    moddate = models.DateField("last modified date")

    def save(self,*args, **kwargs):
        # if it doesn't have id
        if not self.id:
            self.pubdate = timezone.now()
        # last modifed date
        self.moddate = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def toggle_like(self, liker):
        if liker not in self.likes.all():
            self.likes.add(liker)
            self.likes_count += 1

        else:
            self.likes.remove(liker)
            self.likes_count -= 1

        self.save()
        

    def add_comment(self, comment):
        if comment not in self.comment_set.all():
            self.comment_set.add(comment)
            self.comments_count += 1
        self.save()

    def remove_comment(self, comment):
        if comment in self.comment_set.all():
            self.comment_set.remove(comment)
            comment.delete()
            self.comments_count -= 1
        self.save()


# comments sent by others
class Comment(models.Model):
    text = models.CharField(max_length=500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text


# responds to a comment
class Respond(models.Model):
    text = models.CharField(max_length=350)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class CssCode(models.Model):
    code = models.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_css_code")
    websiteinfo =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="website_info_css_Code")

# website schema
class WebsiteInfo(models.Model):
    
    #header section
    header_image_addr = models.CharField(max_length=300)
    header_title = models.CharField(max_length=50)
    header_description = models.CharField(max_length=200)

    #navbar section
    navbar_background_color = models.CharField(max_length=100)
    navbar_magic_line_color = models.CharField(max_length=100)


class Feedback(models.Model):
    text = models.CharField(max_length=300)