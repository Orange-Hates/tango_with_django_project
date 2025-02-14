from django.contrib import admin
from rango.models import Category, Page
from django.contrib import admin
from rango.models import UserProfile

admin.site.register(UserProfile)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')  # Custom admin display

admin.site.register(Category)
admin.site.register(Page, PageAdmin)  # Register with custom display
