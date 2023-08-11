from accounts.models import Address
from accounts.forms import AddressForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class AddressCreateView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/addressform.html'
    form_class = AddressForm
    model = Address
    
    def dispatch(self, request, username, pk, *args, **kwargs):
        if request.user.pk != pk:
            return HttpResponseForbidden("You are not allowed to perform this task")
        if request.user.address != None:
            return HttpResponseForbidden("You are not allowed to perform this task. You already have an address")
        return super().dispatch(request, username=username, pk=pk, *args, **kwargs)
    

    def get(self, request, username, pk, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, username, pk, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            instance = form.save()
            instance.users.add(request.user)
            instance.save()
            return redirect("accounts:updateaddress",  instance.id)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        
class UpdateAddressView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/addressform.html'
    form_class = AddressForm
    model = Address
    address = None

    def dispatch(self, request, id, *args, **kwargs):
        if request.user.address == None:
            return HttpResponseForbidden("You are not allowed to perform this task")
        self.address = get_object_or_404(self.model, id=id)
        return super().dispatch(request, id, *args, **kwargs)
    

    def get(self, request, id, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class(instance=self.address)})
    
    def post(self, request, id, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.address)
        if form.is_valid():
            instance = form.save()
            return redirect("accounts:updateaddress",  instance.id)
        
        else:
            return render(request, self.template_name, {"form": form, "errors": form.errors})
