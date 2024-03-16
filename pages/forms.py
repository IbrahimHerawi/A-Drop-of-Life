from django import forms

choices = [
    ("o+", "O+"),
    ("o-", "O-"),
    ("ab+", "AB+"),
    ("ab-", "AB-"),
    ("a+", "A+"),
    ("a-", "A-"),
    ("b+", "B+"),
    ("b-", "B-"),
]


class LookForForm(forms.Form):
    blood_group = forms.ChoiceField(choices=choices, required=True)
    required_volume = forms.IntegerField(label="Required Volume in ml", required=True)

    def clean_required_volume(self):
        required_volume = self.cleaned_data["required_volume"]

        if required_volume <= 0:
            raise forms.ValidationError(
                "The required volume should be a positive number!"
            )

        return required_volume
