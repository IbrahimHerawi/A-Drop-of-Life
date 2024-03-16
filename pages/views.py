from django.views.generic import TemplateView, FormView
from django.shortcuts import render

from bloodbank.models import BloodGroup
from .forms import LookForForm


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutusPageView(TemplateView):
    template_name = "pages/aboutus.html"


class QuestionsPageView(TemplateView):
    template_name = "pages/questions.html"


def LookForView(request):
    if request.method == "POST":
        form = LookForForm(request.POST)
        if form.is_valid():
            available_volume = BloodGroup.objects.get(
                group_name__exact=form.cleaned_data["blood_group"]
            ).available_volume
            required_volume = form.cleaned_data["required_volume"]

            return render(
                request,
                "pages/result.html",
                {
                    "blood_group": form.cleaned_data["blood_group"],
                    "available_volume": available_volume,
                    "required_volume": required_volume,
                },
            )
    else:
        form = LookForForm()
    return render(request, "pages/lookfor.html", {"form": form})
