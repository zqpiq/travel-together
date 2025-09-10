from django.urls import path, include
from account.views import (
    ProfileDetailView,
    PublicProfileDetailView,
    FullProfileDetailView, ProfileEditView, UserRegisterView, ProfileDoneView,
)

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("fill-profile/", ProfileEditView.as_view(), name="fill-profile"),
    path(
        "public_profile/<int:pk>/",
        PublicProfileDetailView.as_view(),
        name="public-profile",
    ),
    path(
        "full-profile/<int:pk>/", FullProfileDetailView.as_view(), name="full-profile"
    ),
    path("profile/done/", ProfileDoneView.as_view(), name="profile-done"),
]
