from accounts.models import AddressModel
from accounts.forms import AddressForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core import serializers

_MODEL = AddressModel

class AddressListView(View):
    def get(self, request, *args, **kwargs):
        if request.headers['X-Requested-With'] ==  'XMLHttpRequest' and request.user.is_authenticated:
            search = request.GET.get("search_value")
            addresses = _MODEL.objects.filter(address_one__icontains=search)
            addresses_ser = serializers.serialize('json', addresses)
            return JsonResponse({"success": True, "data": addresses_ser})
        else:
             return JsonResponse({"success": False, 'message': 'Bad request'}, status=500)

class AddressCreateView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/address/create_form.html'
    form_class = AddressForm
    model = _MODEL
    
    def dispatch(self, request, username, pk, *args, **kwargs):
       
        if request.user.address != None:
            return HttpResponseForbidden("You are not allowed to perform this task. You already have an address")
        return super().dispatch(request, username=username, pk=pk, *args, **kwargs)
    

    def get(self, request, username, pk, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, username, pk, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            address = None
            cd = form.cleaned_data
            if cd["user_address"]:
                address = self.model.objects.get(id=cd["user_address"])
            

            if address != None:
                address.users.add(request.user)
                address.save()
            else:
                address = form.save()
                address.users.add(request.user)
                address.save()

            return redirect("accounts:updateaddress",  address.id)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        
class UpdateAddressView(LoginRequiredMixin, View):
    template_name = 'accounts/manage/address/update_form.html'
    form_class = AddressForm
    model = _MODEL
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
            cd = form.cleaned_data
            if cd["user_address"]:
                address = self.model.objects.get(id=cd["user_address"])
            else:
                address = None

            if address != None:
                self.address.users.remove(request.user)
                address.users.add(request.user)
                address.save()
            else:
                instance = form.save()

            messages.success(request, "Address updated successfully")
            return redirect("accounts:updateaddress",  instance.id)
        
        else:
            messages.error(request, "Address not updated successfully")
            return render(request, self.template_name, {"form": form, "errors": form.errors})
