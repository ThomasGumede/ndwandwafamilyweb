from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("home.urls", namespace="home")),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("campaign/", include("campaign.urls", namespace="campaign")),
    path("event/", include("event.urls", namespace="event")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("payments/", include("payments.urls", namespace="payments")),
    path("actions/", include("actions.urls", namespace="actions")),
    path('tinymce/', include('tinymce.urls')),
    # path("__reload__/", include("django_browser_reload.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
