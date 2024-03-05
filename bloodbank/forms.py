from django import forms

from .models import (
    BloodGroup,
    Donation,
    Request,
)


class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = [
            "group_name",
            "available_volume",
        ]


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
            "transfusion_name",
        ]
