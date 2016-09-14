from django.contrib import admin

# Register your models here.
from app1 import models





admin.site.register(models.Admin)
admin.site.register(models.Chat)
admin.site.register(models.News)
admin.site.register(models.NewsType)
admin.site.register(models.Reply)
admin.site.register(models.UserTypr)