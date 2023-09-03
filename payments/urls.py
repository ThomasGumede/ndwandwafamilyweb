from django.urls import path
from payments.views import ContributionOrderProcessView, TicketOrderProcessView, ContributionOrderPaid, ContributionOrderFailed, ContributionOrderCancelled, TicketOrderCancelled, TicketOrderPaid

app_name = "payments"

urlpatterns = [
    path("contribution-order/<donation_id>", ContributionOrderProcessView.as_view(), name="contribution-order"),
    path("contribution-order/success", ContributionOrderPaid.as_view(), name="contribution-payment-success"),
    path("contribution-order/cancelled", ContributionOrderCancelled.as_view(), name="contribution-payment-cancelled"),
    path("contribution-order/failed", ContributionOrderFailed.as_view(), name="contribution-payment-failed"),
    path("ticket-order/<ticket_id>", TicketOrderProcessView.as_view(), name="tickets-order"),
    path("ticket-order/success", TicketOrderPaid.as_view(), name="tickets-payment-success"),
    path("ticket-order/cancelled", TicketOrderPaid.as_view(), name="tickets-payment-cancelled"),
]
