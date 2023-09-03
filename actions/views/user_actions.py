from django.shortcuts import render, get_object_or_404
from accounts.models import Contact
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import View
from django.core.mail import EmailMessage

User = get_user_model()

    
class FollowUser(View):
    model = get_user_model()
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id", None)
        username = request.POST.get("username", None)
        action = request.POST.get('action')
        if action and user_id:
            user = get_object_or_404(self.model, pk=user_id, username=username)
            if request.user != user:
                if action == 'follow' and request.user not in user.followers.all():
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Can't follow yourself"})
        else:
            return JsonResponse({"success": False}, status=404)