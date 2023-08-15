from accounts.models import NextOfKin
from accounts.forms import NextOfKinForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class NextOfKinCreateView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/nextofkin/create_form.html'
    form_class = NextOfKinForm
    

    def dispatch(self, request, username, *args, **kwargs):
        if request.user.username != username:
            return redirect("home")
        return super().dispatch(request, username=request.user.username, *args, **kwargs)
    
    def get(self, request, *args, username, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, username, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.relative = request.user
            instance.save()
            messages.success(request, "Relative  created successfully")
            return redirect("accounts:addnextofkin", username=request.user.username)
        else:
            messages.success(request, "Relative not created successfully")
            return render(request, self.template_name, {"form": form})
        
class NextOfKinUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/nextofkin/update_form.html'
    form_class = NextOfKinForm
    model = None

    def dispatch(self, request, username, next_of_kin_id, *args, **kwargs):
        if request.user.username != username:
            return redirect("home")
        self.model = get_object_or_404(NextOfKin, id=next_of_kin_id)
        return super().dispatch(request, username=request.user.username, next_of_kin_id=next_of_kin_id, *args, **kwargs)
    
    def get(self, request, *args, username, next_of_kin_id, **kwargs):
        return render(self, request, self.template_name, {"form": self.form_class(instance=self.model)})
    
    def post(self, request, username, next_of_kin_id, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.model)
        if form.is_valid():
            instance = form.save()
            instance.save()
            messages.success(request, f"Relative {instance.full_name} updated successfully")
            return redirect("accounts:updatenextofkin", username=request.user.username, next_of_kin_id = self.model.id)
        else:
            messages.success(request, "Relative not updated successfully")
            return render(self, request, self.template_name, {"form": form})
