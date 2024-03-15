from django.shortcuts import redirect, render
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
    StateMaintainingForm,
)


# Dashboard View
class DashboardView(ListView):
    model = BloodGroup
    template_name = "bloodbank/general/dashboard.html"


# Blood Groups View
class BloodGroupsView(ListView):
    model = BloodGroup
    template_name = "bloodbank/general/bloodgroups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        begin = self.request.GET.get("begin")
        end = self.request.GET.get("end")

        if (begin is None and end is None) or (begin == "" and end == ""):
            for bg in context["object_list"]:
                donations = Donation.objects.filter(blood_group=bg.id).count()
                requests = Request.objects.filter(blood_group=bg.id).count()
                bg.donations = donations
                bg.requests = requests
            return context

        elif begin is None or begin == "":
            for bg in context["object_list"]:
                donations = (
                    Donation.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__lte=end)
                    .count()
                )
                requests = (
                    Request.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__lte=end)
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context

        elif end is None or end == "":
            for bg in context["object_list"]:
                donations = (
                    Donation.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__gte=begin)
                    .count()
                )
                requests = (
                    Request.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__gte=begin)
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context

        else:
            for bg in context["object_list"]:
                donations = (
                    Donation.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__range=(begin, end))
                    .count()
                )
                requests = (
                    Request.objects.filter(blood_group=bg.id)
                    .filter(transfusion_date__range=(begin, end))
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context


# Donation Views
class DonationListView(ListView):
    model = Donation
    template_name = "bloodbank/donation/donation_list.html"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query is None:
            queryset = Donation.objects.all().order_by("status", "-transfusion_date")
            return queryset

        if status == "0":
            queryset = Donation.objects.filter(donor_name__icontains=query).order_by(
                "status", "-transfusion_date"
            )
            return queryset

        queryset = (
            Donation.objects.filter(status__exact=status)
            .filter(donor_name__icontains=query)
            .order_by("status", "-transfusion_date")
        )

        return queryset


class DonationCreateView(CreateView):
    model = Donation
    template_name = "bloodbank/donation/donation_new.html"
    form_class = DonationForm
    success_url = reverse_lazy("donation-list")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        residual_volume = cleaned_data["donation_volume"]

        donation = form.save(commit=False)
        donation.residual_volume = residual_volume
        donation.status = "1"

        donation.save()

        return super().form_valid(form)


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
    paginate_by = 5

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
    success_url = reverse_lazy("state-maintaining")


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


def StateMaintainingView(request):
    if request.method == "POST":
        form = StateMaintainingForm(request.POST)
        if "save_and_add_another" in request.POST and form.is_valid():
            donor_id = form.cleaned_data["donor_id"]
            donor = Donation.objects.get(id=donor_id)
            volume_taken = form.cleaned_data["volume_taken"]

            donor.residual_volume = donor.residual_volume - volume_taken

            if donor.residual_volume < 50:
                donor.status = "2"

            donor.save()
            form = StateMaintainingForm()

        elif form.is_valid():
            donor_id = form.cleaned_data["donor_id"]
            donor = Donation.objects.get(id=donor_id)
            volume_taken = form.cleaned_data["volume_taken"]

            donor.residual_volume = donor.residual_volume - volume_taken

            if donor.residual_volume < 50:
                donor.status = "2"

            donor.save()
            return redirect("request-list")
    else:
        form = StateMaintainingForm()
    return render(request, "bloodbank/request/state_maintaining.html", {"form": form})
