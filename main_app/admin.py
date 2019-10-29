from django.contrib import admin
from django.contrib.auth import get_user_model
from  .models import Item, Profile, Comment
# Register your models here.

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Comment)