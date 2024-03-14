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
    donor_id = forms.IntegerField(required=True)
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
