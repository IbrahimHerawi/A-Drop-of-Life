from datetime import date
from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.urls import reverse


# Blood Group Table
class BloodGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(
        max_length=5,
        choices=[
            ("o+", "O+"),
            ("o-", "O-"),
            ("ab+", "AB+"),
            ("ab-", "AB-"),
            ("a+", "A+"),
            ("a-", "A-"),
            ("b+", "B+"),
            ("b-", "B-"),
        ],
    )

    @property
    def available_volume(self):
        try:
            amount = (
                Donation.objects.exclude(status=2)
                .filter(blood_group=self.id)
                .aggregate(models.Sum("residual_volume"))
            )

            if amount["residual_volume__sum"] is None:
                amount = 0
                return amount

            return amount["residual_volume__sum"]

        except:
            amount = 0
            return amount

    def __str__(self):
        return self.group_name


# Donor Table
class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    id_num = models.CharField(
        unique=True,
        validators=[RegexValidator("(^[0-9]{4}-[0-9]{4}-[0-9]{5}$)|(^[0-9]{8}$)")],
    )
    donor_name = models.CharField(max_length=500)
    donor_phone = models.CharField(
        max_length=13, validators=[RegexValidator("^0093\d{9}")]
    )
    donor_email = models.EmailField()
    donor_gender = models.CharField(
        max_length=15, choices=(("Male", "Male"), ("Female", "Female"))
    )
    donor_date_of_birth = models.DateField()
    donor_address = models.TextField(blank=True, null=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)

    @property
    def age(self):
        today = date.today()
        age = (
            today.year
            - self.donor_date_of_birth.year
            - (
                (today.month, today.day)
                < (self.donor_date_of_birth.month, self.donor_date_of_birth.day)
            )
        )
        return age

    def __str__(self):
        return f"{self.donor_name}-{self.blood_group.group_name}"

    def get_absolute_url(self):
        return reverse("donor-edit", kwargs={"pk": self.id})


# Donations Table
class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    donation_volume = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(460)]
    )
    residual_volume = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(460)]
    )
    transfusion_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[("1", "Valid"), ("2", "Invalid")])
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.donor.donor_name}-{self.blood_group.group_name}"

    def get_absolute_url(self):
        return reverse("donation-detail", kwargs={"pk": self.pk})

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["status"]),
        ]


# Requests Table
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=500)
    patient_phone = models.CharField(
        max_length=13, validators=[RegexValidator("^0093\d{9}")]
    )
    patient_email = models.EmailField()
    patient_gender = models.CharField(
        max_length=15, choices=(("Male", "Male"), ("Female", "Female"))
    )
    patient_age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(150)])
    patient_address = models.TextField(blank=True, null=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    volume = models.PositiveSmallIntegerField()
    transfusion_date = models.DateTimeField(auto_now_add=True)
    physician_name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name}-{self.blood_group.group_name}"

    def get_absolute_url(self):
        return reverse("request-detail", kwargs={"pk": self.pk})
