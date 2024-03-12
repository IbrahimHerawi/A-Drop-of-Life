from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import (
    BloodGroup,
    Donation,
    Request,
)
from .forms import (
    DonationForm,
    UpdateDonationForm,
    RequestForm,
)


# Dashboard View
class DashboardView(ListView):
    model = BloodGroup
    template_name = "bloodbank/general/dashboard.html"


# Blood Groups View
class BloodGroupsView(ListView):
    model = BloodGroup
    template_name = "bloodbank/general/bloodgroups.html"


# Donation Views
class DonationListView(ListView):
    model = Donation
    template_name = "bloodbank/donation/donation_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query is None:
            queryset = Donation.objects.all().order_by("-transfusion_date")
            return queryset

        if status == "0":
            queryset = Donation.objects.filter(donor_name__icontains=query).order_by(
                "-transfusion_date"
            )
            return queryset

        queryset = (
            Donation.objects.filter(status__exact=status)
            .filter(donor_name__icontains=query)
            .order_by("-transfusion_date")
        )

        return queryset


class DonationCreateView(CreateView):
    model = Donation
    template_name = "bloodbank/donation/donation_new.html"
    form_class = DonationForm
    success_url = reverse_lazy("donation-list")


class DonationDetailView(DetailView):
    model = Donation
    template_name = "bloodbank/donation/donation_detail.html"


class DonationEditView(UpdateView):
    model = Donation
    template_name = "bloodbank/donation/donation_edit.html"
    form_class = UpdateDonationForm


class DonationDeleteView(DeleteView):
    model = Donation
    template_name = "bloodbank/donation/donation_delete.html"
    success_url = reverse_lazy("donation-list")


# Request Views
class RequestListView(ListView):
    model = Request
    template_name = "bloodbank/request/request_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query is None:
            queryset = Request.objects.all().order_by("-transfusion_date")
            return queryset

        queryset = Request.objects.filter(patient_name__icontains=query).order_by(
            "-transfusion_date"
        )

        return queryset


class RequestCreateView(CreateView):
    model = Request
    template_name = "bloodbank/request/request_new.html"
    form_class = RequestForm
    success_url = reverse_lazy("request-list")


class RequestDetailView(DetailView):
    model = Request
    template_name = "bloodbank/request/request_detail.html"


class RequestEditView(UpdateView):
    model = Request
    template_name = "bloodbank/request/request_edit.html"
    form_class = RequestForm


class RequestDeleteView(DeleteView):
    model = Request
    template_name = "bloodbank/request/request_delete.html"
    success_url = reverse_lazy("request-list")
