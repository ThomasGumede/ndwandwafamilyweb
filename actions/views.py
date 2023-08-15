from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import DetailView, View, FormView, UpdateView


User = get_user_model()

class UserSearchView(View):
    template_name = "search/search.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"results": "results"})