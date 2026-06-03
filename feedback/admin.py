from django.contrib import admin

from .models import (
    Department,
    Faculty,
    FeedBack,
)


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Faculty)
class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(FeedBack)
class FeedBackModelAdmin(admin.ModelAdmin):
    list_display = ["id", "department", "status"]
