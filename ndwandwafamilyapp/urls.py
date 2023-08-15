from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home/home.html"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("campaign/", include("campaign.urls", namespace="campaign")),
    path("event/", include("event.urls", namespace="event")),
    path("actions/", include("actions.urls", namespace="actions")),
    # path("__reload__/", include("django_browser_reload.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
