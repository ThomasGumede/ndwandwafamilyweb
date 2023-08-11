from accounts.models import CustomUser, Wallet
from accounts.forms import AccountUpdateForm, GeneralEditForm, RegistrationForm
from django.http import JsonResponse, HttpResponseForbidden
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model


User = get_user_model()

class AccountsView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = "users"
    template_name = "accounts.html"

class AccountDetailView(LoginRequiredMixin, DetailView):
    queryset = CustomUser.objects.select_related("address").prefetch_related("qualifications", "next_of_kins")
    context_object_name = "user"
    template_name = "account.html"
    slug_field = 'username'
    slug_url_kwarg = 'username'
    query_pk_and_slug = True

class AccountCreateView(View):
    template_name = 'accounts/signup.html'
    form_class = RegistrationForm
    context = {
            "form" : form_class
        }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            instance = form.save()
            Wallet.objects.create(name=f"{instance.username}-wallet", owner=instance)
            instance.save()
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password1'])
            login(self.request, user)
            return redirect("accounts:createaddress", user.username, user.pk)
        else:
            return render(request, self.template_name, {"form": form})

# User update views
class GeneralView(LoginRequiredMixin, View):
    model = None
    form_class = GeneralEditForm
    template_name = "accounts/manage/general.html"

    def get_user(self, username, pk):
        user = get_object_or_404(User, username=username, pk=pk)
        return user

    def dispatch(self, request, username, pk, *args, **kwargs):
        self.model = self.get_user(username, pk)
        if request.user != self.model:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.model)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.model)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.username = cd["username"]
            self.model.email = cd["email"]
            self.model.save(update_fields=["username", "email"])
            messages.success(request, "Username or email updated successfully")
            return redirect("accounts:general_edit", username=self.model.username, pk=self.model.pk)
        else:
            messages.error(request, "Error receives, please fix all below errors")
            return render(request, self.template_name, {"form": form})

class AccountUpdateView(LoginRequiredMixin, View):
    model = None
    form_class = AccountUpdateForm
    template_name = "accounts/manage/user/update_user.html"

    def get_user(self, username, pk):
        user = get_object_or_404(User, username=username, pk=pk)
        return user

    def dispatch(self, request, username, pk, *args, **kwargs):
        self.model = self.get_user(username, pk)
        if request.user != self.model:
            return redirect("accounts:account_details", username=self.model.username, pk=self.model.pk)
        else:
            return super().dispatch(request, username, pk, *args, **kwargs)
        
    def get(self, request, username, pk, *args, **kwargs):
        form = self.form_class(instance=self.model)
        return render(request, self.template_name, {"form": form})

    def post(self, request, username, pk, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.model)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.photo = cd["photo"]
            self.model.biography = cd["biography"]
            self.model.first_name = cd["first_name"]
            self.model.last_name = cd["last_name"]
            self.model.occupation = cd["occupation"]
            self.model.professional_affiliations = cd["professional_affiliations"]
            self.model.save(update_fields=["first_name", "last_name", "occupation", "biography", "professional_affiliations", "photo"])
            messages.success(request, "Account updated successfully")
            return redirect("accounts:update_account", username=self.model.username, pk=self.model.pk)
        else:
            messages.error(request, "Something isn\'t right, please fix below errors")
            return render(request, self.template_name, {"form": form})


class AccountSearchView(LoginRequiredMixin, View):
    model = None
    def dispatch(self, request, *args, **kwargs):
        if request.headers['X-Requested-With'] !=  'XMLHttpRequest':
            return JsonResponse({"success": False, "message": "This request is not allowed"}, safe=True, status=500)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        key = request.GET.get("key")
        users_by_username = User.objects.filter(username__icontains = key)
        users_by_firstname = User.objects.filter(first_name__icontains = key)
        users_by_lastname = User.objects.filter(last_name__icontains=key)

        users_by_username_sr = serializers.serialize("json", users_by_username)
        users_by_firstname_sr = serializers.serialize("json", users_by_firstname)
        users_by_lastname_sr = serializers.serialize("json", users_by_lastname)
        data = {
            "users_by_username_sr" : users_by_username_sr,
            "users_by_firstname_sr" : users_by_firstname_sr,
            "users_by_lastname_sr" : users_by_lastname_sr
        }
        return JsonResponse({"success": True, "data": data}, status=200)

    