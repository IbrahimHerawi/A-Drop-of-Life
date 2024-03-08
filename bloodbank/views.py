from django.views.generic import (
    ListView,
)

from .models import (
    BloodGroup,
)


class DashboardView(ListView):
    model = BloodGroup
    template_name = "bloodbank/dashboard.html"


class BloodGroupsView(ListView):
    model = BloodGroup
    template_name = "bloodbank/bloodgroups.html"
