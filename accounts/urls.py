from accounts.views.account import *
from accounts.views.address import *
from accounts.views.password import *
from accounts.views.qualification import *
from accounts.views.relative import *
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import UserLoginForm
from accounts.views.subscription import *

app_name = "accounts"

urlpatterns = [
    path("", AccountsView.as_view(), name="account_list"),
    path('general/<username>/<pk>', GeneralView.as_view(), name='general_edit'),
    path('reset_password', PwdResetView.as_view(), name='password_reset'),
    path("change_password/<username>/<pk>", UpdatePasswordView.as_view(), name="password_change"),
    path('forgotpassword/<uidb64>/<token>', PwdResetConfirmView.as_view(), name='pwd_reset_confirm'),
    path("details/<username>/<pk>", AccountDetailView.as_view(), name="account_details"),
    path("login", LoginView.as_view(template_name="accounts/login.html", form_class=UserLoginForm, redirect_authenticated_user=True), name="login"),
    path('logout', LogoutView.as_view(next_page="accounts:login"), name='logout'),
    path('signup', AccountCreateView.as_view(), name='signup'),
    path("address_search", AddressListView.as_view(), name="address_search"),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    path('activate', ActivationSentView.as_view(), name="activate_confirmation"),
    
    path("updateaddress/<id>", UpdateAddressView.as_view(), name="updateaddress"),
    path("updatequlification/<int:pk>/<uuid:id>", QualificationUpdateView.as_view(), name="updatequlification"),
    path("update/<username>/<pk>", AccountUpdateView.as_view(), name="update_account"),
    path("updatenextofkin/<username>/<next_of_kin_id>", NextOfKinUpdateView.as_view(), name="updatenextofkin"),

    path("createaddress/<username>/<pk>", AddressCreateView.as_view(), name="createaddress"),
    path("createnextofkin/<username>", NextOfKinCreateView.as_view(), name="addnextofkin"),
    path("createqualification/<pk>", QualificationCreateView.as_view(), name="create_qualification"),

    path("delete_relative/<next_id>", NextOfKinDeleteView.as_view(), name="delete_relative"),
    path("delete_qualification/<qual_id>", QualificationDeleteView.as_view(), name="delete_qualification"),

    path("notifications", MailView.as_view(), name="notifications")


]
