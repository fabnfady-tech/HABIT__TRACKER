from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'color', 'user')
    list_filter   = ('user',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'status', 'priority', 'due_date', 'user', 'category')
    list_filter   = ('status', 'priority', 'category')
    search_fields = ('title', 'description')
# Register your models here.
