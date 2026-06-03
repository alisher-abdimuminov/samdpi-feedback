from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

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


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
