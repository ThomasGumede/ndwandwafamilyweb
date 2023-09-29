from accounts.models import QualificationModel
from accounts.forms import QualificationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class QualificationCreateView(LoginRequiredMixin, View):
    model = QualificationModel
    template_name = "accounts/manage/qualification/create_form.html"
    form_class = QualificationForm

    def get(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "Qualification created successfully")
            return redirect("accounts:create_qualification", pk=pk)
        else:
            messages.success(request, "Qualification not created successfully")
            return render(request, self.template_name, {"form": form})  

class QualificationUpdateView(LoginRequiredMixin, View):
    model = QualificationModel
    template_name = "accounts/manage/qualification/update_form.html"
    form_class = QualificationForm
    qualification = None

    def dispatch(self, request, pk, id, *args, **kwargs):
        if request.user.pk != pk:
            return HttpResponseForbidden()
        self.qualification = get_object_or_404(self.model, id=id)
        return super().dispatch(request, pk, id, *args, **kwargs)
    
    def get(self, request, pk, id, *args, **kwargs):
        form = self.form_class(instance=self.qualification)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, pk, id,*args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.qualification)
        if form.is_valid():
            instance = form.save()
            messages.success(request, "Qualification updated successfully")
            return redirect("accounts:updatequlification", pk=request.user.pk, id=instance.id)
        else:
            messages.success(request, "Qualification not updated successfully")
            return render(request, self.template_name, {"form": form})  
    
class QualificationDeleteView(LoginRequiredMixin, View):
    model = None
    def dispatch(self, request, qual_id,*args, **kwargs):
        if request.headers['X-Requested-With'] !=  'XMLHttpRequest':
            return JsonResponse({"success": False, "message": "This request is not allowed"}, status=500)
        try:
            self.model = QualificationModel.objects.get(id = qual_id)
        except QualificationModel.DoesNotExist:
            return JsonResponse({"success": False, "message": "This qualification is already deleted or does not exists"}, status=200)
        
        return super().dispatch(request, qual_id,*args, **kwargs)
    
    def post(self, request, qual_id, *args, **kwargs):
        
        self.model.delete()
            
        return JsonResponse({"success": True, "message": "Qualification deleted"})