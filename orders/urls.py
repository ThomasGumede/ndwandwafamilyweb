from django.urls import path
from orders.views.contribution_order import ContributionCreateView
from orders.views.ticket_orders import TicketBuyView

app_name = "orders"
urlpatterns = [
    path("contribution-summary/<campaign_id>", ContributionCreateView.as_view(), name="contributions-summary"),
    path("ticket-order-summary/<event_id>", TicketBuyView.as_view(), name="tickets-order-summary")
]
