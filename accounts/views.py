from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .models import CustomUser


class UserEditView(UpdateView):
    model = CustomUser
    fields = (
        "username",
        "email",
        "facility_name",
        "phone_num1",
        "phone_num2",
        "address",
    )
    template_name = "account/profile.html"
    success_url = reverse_lazy("dashboard")
