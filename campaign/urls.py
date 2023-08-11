from django.urls import path
from campaign.views.donation import DonationCreateView
from campaign.views.campaign import CampaignListView, CampaignDetailView, CampaignCreateView, CampaignUpdateView, CampaignDeleteView

app_name = "campaign"
urlpatterns = [
    path("campaigns", CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/<category_id>", CampaignListView.as_view(), name="campaign_list_by_category"),
    path("campaign_details/<id>", CampaignDetailView.as_view(), name="campaign_details"),
    path("campaign_update/<campaign_id>", CampaignUpdateView.as_view(), name="campaign_update"),
    path("delete_campaign/<campaign_uuid>", CampaignDeleteView.as_view(), name="delete_campaign"),
    path("create_campaign", CampaignCreateView.as_view(), name="create_campaign"),
    path("donation/<campaign_id>", DonationCreateView.as_view(), name = "donate")
]
