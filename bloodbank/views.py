from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
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
    Donor,
    Donation,
    Patient,
    Request,
)
from .forms import (
    DonorForm,
    DonationForm,
    UpdateDonationForm,
    PatientForm,
    RequestForm,
    RequestUpdateForm,
    StateMaintainingForm,
)


# Dashboard View
class DashboardView(LoginRequiredMixin, ListView):
    model = BloodGroup
    template_name = "bloodbank/general/dashboard.html"
    login_url = "account_login"


# Blood Groups View
class BloodGroupsView(ListView):
    model = BloodGroup
    template_name = "bloodbank/general/bloodgroups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        begin = self.request.GET.get("begin")
        end = self.request.GET.get("end")
        gender = self.request.GET.get("gender")
        if gender and gender != "all":
            donations_queryset = Donation.objects.filter(donor__donor_gender=gender)
            requests_queryset = Request.objects.filter(patient__patient_gender=gender)
        else:
            donations_queryset = Donation.objects.all()
            requests_queryset = Request.objects.all()

        if begin and end:
            for bg in context["object_list"]:
                donations = (
                    donations_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__range=(begin, end))
                    .count()
                )

                requests = (
                    requests_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__range=(begin, end))
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context
        elif begin:
            for bg in context["object_list"]:
                donations = (
                    donations_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__gte=begin)
                    .count()
                )
                requests = (
                    requests_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__gte=begin)
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context
        elif end:
            for bg in context["object_list"]:
                donations = (
                    donations_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__lte=end)
                    .count()
                )
                requests = (
                    requests_queryset.filter(blood_group=bg.id)
                    .filter(transfusion_date__lte=end)
                    .count()
                )
                bg.donations = donations
                bg.requests = requests
            return context
        else:
            for bg in context["object_list"]:
                donations = donations_queryset.filter(blood_group=bg.id).count()
                requests = requests_queryset.filter(blood_group=bg.id).count()
                bg.donations = donations
                bg.requests = requests
            return context


# Donor Views
class DonorListView(ListView):
    model = Donor
    template_name = "bloodbank/donor/donor_list.html"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        bloodgroup = self.request.GET.get("bg")

        if query is None:
            queryset = Donor.objects.all().order_by("-id")
            return queryset

        if query and query != "":
            query = query.strip()
            queryset = Donor.objects.filter(id_num=query)
            return queryset

        if bloodgroup == "all":
            queryset = Donor.objects.all().order_by("-id")
            return queryset

        queryset = Donor.objects.filter(blood_group__group_name=bloodgroup).order_by(
            "-id"
        )
        return queryset


class DonorCreateView(CreateView):
    model = Donor
    template_name = "bloodbank/donor/donor_new.html"
    form_class = DonorForm
    success_url = reverse_lazy("donor-list")


class DonorEditView(UpdateView):
    model = Donor
    template_name = "bloodbank/donor/donor_edit.html"
    form_class = DonorForm


class DonorDeleteView(DeleteView):
    model = Donor
    template_name = "bloodbank/donor/donor_delete.html"
    success_url = reverse_lazy("donation-list")


# Donation Views
class DonationListView(ListView):
    model = Donation
    template_name = "bloodbank/donation/donation_list.html"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query is None:
            queryset = Donation.objects.select_related("donor").order_by(
                "status", "-transfusion_date"
            )
            return queryset

        if status == "0":
            query = query.strip()
            queryset = (
                Donation.objects.filter(
                    Q(donor__donor_name__icontains=query) | Q(donor__id_num=query)
                )
                .select_related("donor")
                .order_by("status", "-transfusion_date")
            )
            return queryset

        query = query.strip()
        queryset = (
            Donation.objects.filter(status__exact=status)
            .filter(Q(donor__donor_name__icontains=query) | Q(donor__id_num=query))
            .select_related("donor")
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
        donor = Donor.objects.get(id_num=cleaned_data.get("donor_id"))

        donation = form.save(commit=False)
        donation.residual_volume = residual_volume
        donation.donor = donor
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


# Patients Views
class PatientListView(ListView):
    model = Patient
    template_name = "bloodbank/patient/patient_list.html"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        bloodgroup = self.request.GET.get("bg")

        if query is None:
            queryset = Patient.objects.all().order_by("-id")
            return queryset

        if query and query != "":
            query = query.strip()
            queryset = Patient.objects.filter(id_num=query)
            return queryset

        if bloodgroup == "all":
            queryset = Patient.objects.all().order_by("-id")
            return queryset

        queryset = Patient.objects.filter(blood_group__group_name=bloodgroup).order_by(
            "-id"
        )
        return queryset


class PatientCreateView(CreateView):
    model = Patient
    template_name = "bloodbank/patient/patient_new.html"
    form_class = PatientForm
    success_url = reverse_lazy("patient-list")


class PatientEditView(UpdateView):
    model = Patient
    template_name = "bloodbank/patient/patient_edit.html"
    form_class = PatientForm


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = "bloodbank/patient/patient_delete.html"
    success_url = reverse_lazy("patient-list")


# Request Views
class RequestListView(ListView):
    model = Request
    template_name = "bloodbank/request/request_list.html"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query is None:
            queryset = Request.objects.select_related("patient").order_by(
                "-transfusion_date"
            )
            return queryset

        query = query.strip()
        queryset = (
            Request.objects.filter(
                Q(patient__patient_name__icontains=query) | Q(patient__id_num=query)
            )
            .select_related("patient")
            .order_by("-transfusion_date")
        )

        return queryset


class RequestCreateView(CreateView):
    model = Request
    template_name = "bloodbank/request/request_new.html"
    form_class = RequestForm
    success_url = reverse_lazy("state-maintaining")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        patient_id = cleaned_data.get("patient_id")
        patient = Patient.objects.get(id_num=patient_id)

        request = form.save(commit=False)
        request.patient = patient

        request.save()

        return super().form_valid(form)


class RequestDetailView(DetailView):
    model = Request
    template_name = "bloodbank/request/request_detail.html"


class RequestEditView(UpdateView):
    model = Request
    template_name = "bloodbank/request/request_edit.html"
    form_class = RequestUpdateForm


class RequestDeleteView(DeleteView):
    model = Request
    template_name = "bloodbank/request/request_delete.html"
    success_url = reverse_lazy("request-list")


def StateMaintainingView(request):
    if request.method == "POST":
        form = StateMaintainingForm(request.POST)
        if "save_and_add_another" in request.POST and form.is_valid():
            donation_id = form.cleaned_data["donation_id"]
            donation = Donation.objects.get(id=donation_id)
            volume_taken = form.cleaned_data["volume_taken"]

            donation.residual_volume = donation.residual_volume - volume_taken

            if donation.residual_volume < 50:
                donation.status = "2"

            donation.save()
            form = StateMaintainingForm()

        elif form.is_valid():
            donation_id = form.cleaned_data["donation_id"]
            donation = Donation.objects.get(id=donation_id)
            volume_taken = form.cleaned_data["volume_taken"]

            donation.residual_volume = donation.residual_volume - volume_taken

            if donation.residual_volume < 50:
                donation.status = "2"

            donation.save()
            return redirect("request-list")
    else:
        form = StateMaintainingForm()
    return render(request, "bloodbank/request/state_maintaining.html", {"form": form})
