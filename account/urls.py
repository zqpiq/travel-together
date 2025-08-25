from django.urls import path, include
from account.views import (
    register,
    fill_profile,
    ProfileDetailView,
    PublicProfileDetailView,
    FullProfileDetailView,
)

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("fill-profile/", fill_profile, name="fill-profile"),
    path(
        "public_profile/<int:pk>/",
        PublicProfileDetailView.as_view(),
        name="public-profile",
    ),
    path(
        "full-profile/<int:pk>/", FullProfileDetailView.as_view(), name="full-profile"
    ),
]
