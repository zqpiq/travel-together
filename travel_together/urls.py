from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("travels.urls", namespace="travels")),
    path("account/", include("account.urls")),
]
