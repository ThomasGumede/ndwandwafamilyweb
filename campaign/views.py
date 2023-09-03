from django.http import HttpResponseServerError, HttpResponseForbidden,  JsonResponse
from django.urls import reverse_lazy
from campaign.models import Campaign, Category
from campaign.forms import CampaignForm
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CampaignListView(View):
    
    template_name = "campaign/campaigns.html"

    def get(self, request, category_id=None, *args, **kwargs):

        query = request.GET.get("q", None)
        query_by = request.GET.get("search_by", None)

        if category_id:
            category = get_object_or_404(Category, id = category_id )

        if query and query_by and category_id:
            
            match query_by:
                case "title":
                    queryset = Campaign.objects.filter(category=category).filter(title__icontains = query).order_by("-creation_date").select_related("creator", "category")
                case _:
                    queryset = Campaign.objects.filter(category=category).filter(title__icontains = query).order_by("-creation_date").select_related("creator", "category")
        elif query and query_by:
            match query_by:
                case "title":
                    queryset = Campaign.objects.filter(title__icontains = query).order_by("-creation_date").select_related("creator", "category")
                case _:
                    queryset = Campaign.objects.filter(title__icontains = query).order_by("-creation_date").select_related("creator", "category")
        elif category_id:
            queryset = Campaign.objects.filter(category=category).order_by("-creation_date").select_related("creator", "category")
        else:
            queryset = Campaign.objects.all().order_by("-creation_date").select_related("creator", "category")

        return render(request, self.template_name, {"campaigns": queryset, "query": query, "query_by": query_by})
    

class CampaignDetailView(DetailView):
    queryset = Campaign.objects.select_related("creator", "category").prefetch_related("contribution_orders")
    template_name = "campaign/campaign.html"
    context_object_name = "campaign"
    slug_field = 'slug'
    slug_url_kwarg = 'campaign_slug'

class CampaignCreateView(LoginRequiredMixin, View):
    template_name = "campaign/manage/create.html"
    form_class = CampaignForm
    categories = Category.objects.all()


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class, "categories": self.categories})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
                campaign = form.save(commit=False)
                campaign.creator = request.user
                campaign.save()
                messages.success(request, "Campaign was created successfully")
                return redirect("campaign:campaign_details", campaign_slug=campaign.slug)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form, "categories": self.categories})

class CampaignUpdateView(LoginRequiredMixin, View):
    template_name = "campaign/manage/update.html"
    form_class = CampaignForm
    model = None
    categories = Category.objects.all()

    def dispatch(self, request, campaign_id, *args, **kwargs):
        
        self.model = get_object_or_404(Campaign, id=campaign_id)
        if request.user != self.model.creator:
            return HttpResponseForbidden()
        return super().dispatch(request, campaign_id=campaign_id, *args, **kwargs)
    
    def get(self, request, campaign_id, *args, **kwargs):
        form = self.form_class(instance=self.model)
        return render(request, self.template_name, {"form": form, "categories": self.categories})
    
    def post(self, request, campaign_id, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.model)
        if form.is_valid:
            instance = form.save()
            instance.save()
            return redirect("campaign:campaign_details", campaign_slug=instance.slug)
        else:
            return render(request, self.template_name, {"form": form, "categories": self.categories})
            
class CampaignDeleteView(LoginRequiredMixin, View):
    model = None

    def dispatch(self, request, campaign_uuid, *args, **kwargs):
       
        self.model = Campaign.objects.get(id = campaign_uuid)

        if self.model == None or self.model.creator.pk != request.user.pk:
            return JsonResponse(data={"success": False, "message": "Campaign not found"}, status=404)
        if self.model.current_amount / self.model.target >= 0.25:
            return JsonResponse(data={"success": False, "message": "You cannot delete this campaign, you have received more that 25% of donations"})
        return super().dispatch(request, campaign_uuid=campaign_uuid, *args, **kwargs)
    
    def post(self, request, campaign_uuid, *args, **kwargs):
        if self.model != None:
            self.model.delete()
            return JsonResponse(data = {'success': True, "message": "Campaign deleted successfully", "url": reverse_lazy("campaign:campaign_list")}, status=200)
        else:
            return JsonResponse(data={"success": False, "message": "Something went wrong on our side, campaign was not removed", "url": reverse_lazy("campaign:campaign_list")}, status=500)
    