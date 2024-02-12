from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Major, Course

admin.site.register(Major)
admin.site.register(Course)
