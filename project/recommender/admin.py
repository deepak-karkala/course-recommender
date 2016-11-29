from django.contrib import admin

# Register your models here.
from .models import Course, User, Rating

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Rating)