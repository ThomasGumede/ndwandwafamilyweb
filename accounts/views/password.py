from django.urls import reverse_lazy
from accounts.forms import PwdResetConfirmForm, PwdResetForm
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.forms import PasswordChangeForm

class UpdatePasswordView(LoginRequiredMixin, View):

    form_class = PasswordChangeForm
    template_name = "accounts/manage/password/change_password.html"

    def get(self, request, username, pk, *args, **kwargs):
        
        return render(request, self.template_name, {"form": self.form_class(request.user)})

    def post(self, request, username, pk, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect("accounts:password_change", username = user.username, pk=user.pk)
        else:
            messages.error(request, 'Error receives, please fix all below errors')
            return render(request, self.template_name, {"form": form})

class PwdResetView(PasswordResetView):
    template_name='accounts/manage/password/pwd__reset_form.html'
    form_class=PwdResetForm
    success_url=reverse_lazy("accounts:login")
    context_object_name = "form"
    email_template_name="accounts/email/password/pwd__reset_email.html"

    def form_invalid(self, form):
        messages.error(self.request, "Something isn\'t right, please fix below errors")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Email sent with password reset instructions")
        return super().form_valid(form)


class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/manage/password/pwd__reset_confirm.html'
    success_url = reverse_lazy('accounts:login')
    form_class=PwdResetConfirmForm

    def form_invalid(self, form):
        messages.error(self.request, "Something isn\'t right, please fix below errors")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Password reset successfully")
        return super().form_valid(form)

