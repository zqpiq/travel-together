from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from account.forms import UserRegistrationForm, ProfileEditForm
from account.models import Profile



class UserRegisterView(generic.FormView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("fill-profile")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        login(self.request, new_user)
        Profile.objects.create(user=new_user)
        return redirect(self.get_success_url())


class ProfileEditView(generic.UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "registration/profile_edit.html"
    success_url = reverse_lazy("profile-done")

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileDoneView(generic.FormView):
    template_name = "registration/register_done.html"
    form_class = ProfileEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user.profile
        return kwargs


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = "registration/profile_detail.html"

    def get_object(self):
        return self.request.user.profile


class PublicProfileDetailView(generic.DetailView):
    model = Profile
    template_name = "registration/public_profile_detail.html"


class FullProfileDetailView(generic.DetailView):
    model = Profile
    template_name = "registration/full_profile_detail.html"
    context_object_name = "profile"
