from django.views.generic import TemplateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from allauth.account.views import EmailView as AllauthEmailView
from .models import UserProfile
from .forms import ProfileUpdateForm, AvatarUploadForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile"
        # Ensure profile exists
        if not hasattr(self.request.user, "profile"):
            UserProfile.objects.create(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        # Check if this is an HTMX request
        if hasattr(request, "htmx") and request.htmx:
            if request.htmx.target == "email-settings-card":
                # Return just the email settings card
                return render(
                    request,
                    "partials/htmx/_email_settings_default.html",
                    self.get_context_data(),
                )
            elif request.htmx.target == "profile-content":
                # Return just the profile cards partial
                return render(
                    request,
                    "partials/htmx/_profile_cards.html",
                    self.get_context_data(),
                )
        return super().get(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        # Get or create profile for current user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


class EmailManagementView(LoginRequiredMixin, AllauthEmailView):
    """Custom email view that handles HTMX requests"""

    def get_template_names(self):
        # Check if this is an HTMX request
        if hasattr(self.request, "htmx") and self.request.htmx:
            return ["partials/htmx/_email_management_card.html"]
        return super().get_template_names()

    def get_success_url(self):
        # For HTMX requests, return to the same view
        if hasattr(self.request, "htmx") and self.request.htmx:
            return reverse_lazy("users:email_management")
        return super().get_success_url()

    def form_valid(self, form):
        """Handle form submission and return updated card"""
        response = super().form_valid(form)
        if hasattr(self.request, "htmx") and self.request.htmx:
            # Return the updated email management card
            return render(
                self.request,
                "partials/htmx/_email_management_card.html",
                self.get_context_data(),
            )
        return response

    def post(self, request, *args, **kwargs):
        """Handle POST requests for email actions"""
        if hasattr(request, "htmx") and request.htmx:
            # Process the action and return updated card
            response = super().post(request, *args, **kwargs)
            # Always return the card template for HTMX requests
            return render(
                request,
                "partials/htmx/_email_management_card.html",
                self.get_context_data(),
            )
        return super().post(request, *args, **kwargs)


class AvatarUploadView(LoginRequiredMixin, FormView):
    """HTMX-aware view for avatar upload."""

    form_class = AvatarUploadForm
    template_name = "partials/htmx/_avatar_upload.html"
    success_url = reverse_lazy("users:profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_profile()
        return kwargs

    def get_profile(self):
        """Get or create user profile."""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        """Handle successful form submission."""
        form.save()

        # Return success partial for HTMX
        if hasattr(self.request, "htmx") and self.request.htmx:
            context = {
                "user": self.request.user,
                "profile": self.get_profile(),
                "success_message": "Avatar updated successfully!",
            }
            response = render(
                self.request, "users/partials/_profile_info_card.html", context
            )
            # Trigger event to refresh the upload form
            response["HX-Trigger"] = "avatar-updated"
            return response

        messages.success(self.request, "Avatar updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors."""
        if hasattr(self.request, "htmx") and self.request.htmx:
            # Return form with errors for HTMX
            return render(
                self.request,
                "partials/htmx/_avatar_upload.html",
                {"form": form, "error": True},
                status=400,
            )
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        """Handle GET requests - show upload form."""
        if hasattr(request, "htmx") and request.htmx:
            form = self.get_form()
            return render(
                request,
                "partials/htmx/_avatar_upload.html",
                {"form": form, "profile": self.get_profile()},
            )
        return super().get(request, *args, **kwargs)
