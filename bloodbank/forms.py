from datetime import date
from typing import Any
from django import forms
from django.core.validators import (
    RegexValidator,
)
from .models import (
    Donor,
    Donation,
    Request,
)


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ["id"]
        labels = {
            "id_num": "ID Number",
            "donor_date_of_birth": "Date of Birth",
        }
        widgets = {"donor_date_of_birth": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        donor_bd = self.cleaned_data["donor_date_of_birth"]
        today = date.today()
        age = (
            today.year
            - donor_bd.year
            - ((today.month, today.day) < (donor_bd.month, donor_bd.day))
        )
        if age < 18 or age > 65:
            raise forms.ValidationError("Donor Age Should be between 18 and 65 years!")


class DonationForm(forms.ModelForm):
    donor_id = forms.CharField(
        label="Donor ID Number",
        validators=[RegexValidator("(^[0-9]{4}-[0-9]{4}-[0-9]{5}$)|(^[0-9]{8}$)")],
    )

    class Meta:
        model = Donation
        exclude = [
            "id",
            "residual_volume",
            "transfusion_date",
            "donor",
            "status",
        ]

    def clean(self):
        donor = self.cleaned_data["donor_id"]
        donation_bg = self.cleaned_data.get("blood_group")

        try:
            donor = Donor.objects.get(id_num=donor)
        except:
            raise forms.ValidationError("This donor does not exist!")

        if donor.blood_group != donation_bg:
            raise forms.ValidationError(
                "Donor's blood group is not of this blood group!"
            )

        if donor.age < 18 or donor.age > 65:
            raise forms.ValidationError(
                "This donor has passed the legal age to donate!"
            )

        return super().clean()


class UpdateDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = [
            "id",
            "transfusion_date",
            "donor",
            "blood_group",
        ]

    def clean_residual_volume(self):
        residual_volume = self.cleaned_data["residual_volume"]
        donation_volume = self.cleaned_data["donation_volume"]

        if residual_volume > donation_volume:
            raise forms.ValidationError(
                "Residual volume should be either equal to or less than donation volume!"
            )

        return residual_volume


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


class StateMaintainingForm(forms.Form):
    donation_id = forms.IntegerField(required=True)
    volume_taken = forms.IntegerField(required=True, max_value=460, min_value=50)

    def clean_donor_id(self):
        try:
            donor = Donation.objects.filter(status="1").get(
                id=self.cleaned_data.get("donor_id")
            )
        except:
            self.add_error("donor_id", "This donor does not exist!")
            raise forms.ValidationError("")

        return self.cleaned_data.get("donor_id")

    def clean_volume_taken(self):

        volume_taken = self.cleaned_data.get("volume_taken")
        try:
            donor = Donation.objects.filter(status="1").get(
                id=self.cleaned_data.get("donor_id")
            )
        except:
            return volume_taken

        if donor.residual_volume < volume_taken:
            self.add_error(
                "volume_taken", "The residual volume of this donor is not enough!!"
            )
            raise forms.ValidationError("")

        return volume_taken
