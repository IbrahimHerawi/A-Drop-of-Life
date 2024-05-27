from django.test import TestCase
from django.urls import reverse

from .models import Donor, BloodGroup


class DonorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.bg = BloodGroup.objects.create(group_name="o+")
        cls.donor = Donor.objects.create(
            id_num="1400-1000-00000",
            donor_name="Jamal",
            donor_phone="0093792552999",
            donor_email="Jamal@gmail.com",
            donor_gender="Male",
            donor_date_of_birth="2000-08-15",
            blood_group=cls.bg,
        )

    def test_donor_createview(self):
        response = self.client.post(
            reverse("donor-new"),
            {
                "id_num": "1400-2000-00000",
                "donor_name": "ahmad",
                "donor_phone": "0093792552777",
                "donor_email": "ahmad@gmail.com",
                "donor_gender": "Male",
                "donor_date_of_birth": "2002-07-15",
                "blood_group": 4,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Donor.objects.last().donor_name, "ahmad")
        self.assertEqual(Donor.objects.last().donor_email, "ahmad@gmail.com")

    def test_donor_editview(self):
        response = self.client.post(
            reverse("donor-edit", args="1"),
            {
                "id_num": "1400-1000-00000",
                "donor_name": "khalid",
                "donor_phone": "0093792552999",
                "donor_email": "khalid@gmail.com",
                "donor_gender": "Male",
                "donor_date_of_birth": "2000-08-15",
                # "donor_address": "Herat",
                "blood_group": 1,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Donor.objects.get(id=1).donor_name, "khalid")
        self.assertEqual(Donor.objects.get(id=1).donor_email, "khalid@gmail.com")
