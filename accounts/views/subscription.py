from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View
from accounts.forms import SubscribeForm
from accounts.models import MailingGroup


class MailView(View):
    template_name = "accounts/manage/notification/index.html"
    form_class = SubscribeForm

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name, {"form": self.form_class, "mailinggroups": MailingGroup.objects.all()})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class, "mailinggroups": MailingGroup.objects.all()})