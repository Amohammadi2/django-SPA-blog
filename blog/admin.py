from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Respond)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(CssCode)
admin.site.register(WebsiteInfo)
admin.site.register(Feedback)