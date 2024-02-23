from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutusPageView(TemplateView):
    template_name = "pages/aboutus.html"


class QuestionsPageView(TemplateView):
    template_name = "pages/questions.html"
