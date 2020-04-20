from django.urls import path
from .views import *
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# registering the post view set here
router.register(r"posts", postsView)
router.register(r"comments", CommentView)
router.register(r"responds", RespondView)
router.register(r"websiteinfo", WebsiteInfoView)
router.register(r"feedbacks", FeedbackView)
router.register(r"categories", CategoryView)
router.register(r"profiles", ProfileView)

urlpatterns = [
    # start page
    path("setuptools/quick_start/", quick_start, name="quick_start"),
    path("", index, name="index"),
    path("<str:template>", render_template),
    path("login/", login_user, name="loginuser"),
    path("logout/", logout_user, name="logoutuser"),
    path("has_account/", has_account, name="hasaccount"),
    path("signup/", signup, name="signup"),
] + router.urls # other urls using viewsets
