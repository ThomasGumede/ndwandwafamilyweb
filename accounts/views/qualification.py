from accounts.models import Qualification
from accounts.forms import QualificationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class QualificationCreateView(LoginRequiredMixin, View):
    model = Qualification
    template_name = "accounts/manage/user/qualification_create.html"
    form_class = QualificationForm

    def get(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})
    
    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect("accounts:create_qualification", pk=pk)
        else:
            return render(request, self.template_name, {"form": form})  

class QualificationUpdateView(LoginRequiredMixin, View):
    model = Qualification
    template_name = "accounts/manage/user/qualification_create.html"
    form_class = QualificationForm
    qualification = None

    def dispatch(self, request, pk, id, *args, **kwargs):
        if request.user.pk != pk:
            return redirect("accounts:account_list")
        
        self.qualification = get_object_or_404(self.model, id=id)
        return super().dispatch(request, pk, id, *args, **kwargs)
    
    
    def get(self, request, pk, id, *args, **kwargs):
        form = self.form_class(instance=self.qualification)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, pk, id,*args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.qualification)
        if form.is_valid():
            instance = form.save()
            return redirect("accounts:updatequlification", pk=request.user.pk, id=instance.id)
        else:
            return render(request, self.template_name, {"form": form})  
    
