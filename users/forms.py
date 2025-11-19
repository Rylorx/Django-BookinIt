from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserDetailsForm(forms.ModelForm):

    # Adds an image field for our profile image
    # profile_image = forms.ImageField(required=False, help_text="Upload a .jpg profile image")

    reading_goal = forms.IntegerField(
        required=False,
        min_value=0,
        label="Reading Goal",
        help_text="Set your reading goal (number of books)"
    )
    display_reading_goal = forms.BooleanField(
        required=False,
        label="Display Reading Goal",
        help_text="Check this box to display your reading goal on your profile"
    )

    # fields removed profile_image"
    # help_texts removed "profile_image": "Upload a .jpg profile image",

    class Meta:
        model = Profile
        fields = ["reading_goal", "display_reading_goal"]
        help_texts = {
            "reading_goal": "Set your reading goal (number of books)",
            "display_reading_goal": "Check this box to display your reading goal on your profile"
        }

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get("profile_image", False)
        if profile_image:
            extension = profile_image.name.split(".")[-1].lower()
            if profile_image.size > 5*1024*1024:
                raise forms.ValidationError("Image file too large ( > 1)")
            if extension != "jpg":
                raise forms.ValidationError("Image file must be of type .jpg")
        return profile_image

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {"username": "", "email": ""}