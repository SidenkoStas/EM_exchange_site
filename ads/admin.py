from django.contrib import admin
from .models import Category, Ad


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "category", "title", "description", "condition",
        "created_at"
    )