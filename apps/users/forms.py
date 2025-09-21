from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    Handles both User email and UserProfile fields.
    """

    email = forms.EmailField(
        disabled=True, help_text="Email cannot be changed here. Use Email Settings."
    )
    first_name = forms.CharField(
        max_length=150, required=False, help_text="Your first name"
    )
    last_name = forms.CharField(
        max_length=150, required=False, help_text="Your last name"
    )

    class Meta:
        model = UserProfile
        fields = ["bio", "phone_number", "date_of_birth", "address", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "avatar": forms.FileInput(attrs={"accept": "image/*"}),
        }
        help_texts = {
            "bio": "Tell us about yourself",
            "phone_number": "Your contact number",
            "date_of_birth": "Your date of birth",
            "address": "Your address",
            "avatar": "Upload your profile picture (max 5MB)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Tailwind classes to all fields
        tailwind_classes = "mt-1 block w-full rounded-md bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = tailwind_classes

        # Populate User email and names from profile
        if self.instance and self.instance.pk:
            self.fields["email"].initial = self.instance.user.email
            self.fields["first_name"].initial = self.instance.first_name
            self.fields["last_name"].initial = self.instance.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update profile name fields
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]

        if commit:
            profile.save()

        return profile


class AvatarUploadForm(forms.ModelForm):
    """
    Dedicated form for avatar upload via HTMX.
    Includes file validation for size and type.
    """

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

    class Meta:
        model = UserProfile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "class": "hidden",
                    "x-ref": "fileInput",
                }
            ),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar:
            # Check file size first
            if hasattr(avatar, "size") and avatar.size > self.MAX_FILE_SIZE:
                raise ValidationError(
                    f"File too large. Maximum size is {self.MAX_FILE_SIZE // (1024*1024)}MB."
                )

            # Check file extension
            if hasattr(avatar, "name"):
                ext = avatar.name.split(".")[-1].lower()
                if ext not in self.ALLOWED_EXTENSIONS:
                    raise ValidationError(
                        f'Unsupported file extension. Allowed: {", ".join(self.ALLOWED_EXTENSIONS)}'
                    )

            # Verify it's a valid image using Pillow
            # This check will catch malformed files
            try:
                width, height = get_image_dimensions(avatar)
                if not width or not height:
                    raise ValidationError("Invalid image file.")
            except Exception:
                # If it's not a valid image, check if it's a size or extension issue
                if hasattr(avatar, "size") and avatar.size > self.MAX_FILE_SIZE:
                    raise ValidationError(
                        f"File too large. Maximum size is {self.MAX_FILE_SIZE // (1024*1024)}MB."
                    )
                elif hasattr(avatar, "name"):
                    ext = avatar.name.split(".")[-1].lower()
                    if ext not in self.ALLOWED_EXTENSIONS:
                        raise ValidationError(
                            f'Unsupported file extension. Allowed: {", ".join(self.ALLOWED_EXTENSIONS)}'
                        )
                raise ValidationError("File is not a valid image.")

        return avatar
