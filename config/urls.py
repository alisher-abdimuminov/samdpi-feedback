from django.contrib import admin
from django.urls import path

from feedback.views import (
    landing,
    faculties_view,
    departments_view,
    ratings_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("ratings/", ratings_view, name="ratings"),
    path("faculties/", faculties_view, name="faculties"),
    path("faculties/<int:pk>/departments/", departments_view, name="departments"),
]
