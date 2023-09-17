from accounts.models import WalletModel
from accounts.forms import AccountUpdateForm, GeneralEditForm, RegistrationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from accounts.tokens import account_activation_token
# from accounts.backends import EmailBackend


User = get_user_model()


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email \n{to_email} inbox and click on \
                received activation link to confirm and complete the registration. \nNote: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


class AccountsView(LoginRequiredMixin, View):
    
    context_object_name = "users"
    template_name = "accounts.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        query_by = request.GET.get("search_by")
        queryset = User.objects
        if query != None:
            match query_by:
                case "first_name":
                    queryset = User.objects.filter(first_name__icontains = query)
                case "last_name":
                    queryset = User.objects.filter(last_name__icontains = query)
                case "username":
                    queryset = User.objects.filter(username__icontains = query)
                case "occupation":
                    queryset = User.objects.filter(occupation__icontains = query)
                case "professional_affiliations":
                    queryset = User.objects.filter(professional_affiliations__icontains = query)
                case "province":
                    queryset = User.objects.filter(address__state__icontains = query)
                case "zipcode":
                    queryset = User.objects.filter(address__zipcode__icontains = query)
                case "city":
                    queryset = User.objects.filter(address__city__icontains = query)
                case _:
                    queryset = User.objects.filter(first_name__icontains = query)
        
        return render(request, self.template_name, {"users": queryset.only("first_name", "last_name", "username","occupation", "address__state", "photo")})

class AccountDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.select_related("address").prefetch_related("qualifications", "next_of_kins")
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
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            WalletModel.objects.create(name=f"{form.cleaned_data.get('first_name')}-wallet", owner=instance)
            activateEmail(request, instance, form.cleaned_data.get('email'))
            return redirect('accounts:activate_confirmation')
        else:
            return render(request, self.template_name, {"form": form})

class ActivateAccountView(View):
    def dispatch(self, request, uidb64, token, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, uidb64, token, *args, **kwargs)

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Activation link is invalid!")

        return redirect('home:home')

class ActivationSentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "email_confirmation_sent.html")

# User update views
class GeneralView(LoginRequiredMixin, View):
    model = None
    form_class = GeneralEditForm
    template_name = "accounts/manage/user/general.html"

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
            self.model.tel = cd["tel"]
            if self.model.id_number != cd["id_number"]:
                return HttpResponseForbidden("You not allowed to update ID number, contact administrator")
            self.model.save(update_fields=["username", "email", "tel"])
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
            print(cd["photo"])
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
