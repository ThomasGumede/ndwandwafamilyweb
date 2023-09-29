from django.urls import path
from payments.views import ContributionOrderProcessView, TicketOrderProcessView, \
ContributionOrderPaid, ContributionOrderFailed, ContributionOrderCancelled, \
TicketOrderCancelled, TicketOrderPaid, TicketOrderFailed

app_name = "payments"

urlpatterns = [
    path("contribution-order/<donation_id>", ContributionOrderProcessView.as_view(), name="contribution-order"),
    path("contribution-payment/success", ContributionOrderPaid.as_view(), name="contribution-payment-success"),
    path("contribution-payment/cancelled", ContributionOrderCancelled.as_view(), name="contribution-payment-cancelled"),
    path("contribution-payment/failed", ContributionOrderFailed.as_view(), name="contribution-payment-failed"),
    
    path("ticket-order/<ticket_id>", TicketOrderProcessView.as_view(), name="tickets-order"),
    path("ticket-payment/success", TicketOrderPaid.as_view(), name="ticket-payment-success"),
    path("ticket-payment/cancelled", TicketOrderCancelled.as_view(), name="ticket-payment-cancelled"),
    path("ticket-payment/cancelled", TicketOrderFailed.as_view(), name="ticket-payment-failed"),
]
