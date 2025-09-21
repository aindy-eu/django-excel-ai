from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Public home page"""

    template_name = "home.html"


class AboutView(TemplateView):
    """Public about page"""

    template_name = "about.html"
