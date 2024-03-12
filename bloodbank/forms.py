from django import forms

from .models import (
    Donation,
    Request,
)


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = [
            "id",
            "residual_volume",
            "transfusion_date",
            "status",
        ]


class UpdateDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = [
            "id",
            "transfusion_date",
        ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        exclude = [
            "id",
            "transfusion_date",
        ]

    def clean_volume(self):
        blood_group = self.cleaned_data.get("blood_group")
        available_volume = blood_group.available_volume

        required_volume = self.cleaned_data.get("volume")

        if required_volume > available_volume:
            raise forms.ValidationError(
                "This volume is not available of this blood group"
            )

        return required_volume
