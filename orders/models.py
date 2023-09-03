from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone
from event.models import Event
from campaign.models import Campaign
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
# Create your models here.

User = get_user_model()
PHONE_REGEX = RegexValidator(
    r'^(\+27|0)[6-8][0-9]{8}$', 'RSA phone number is required')

class PaymentStatus(models.TextChoices):
        PAID = ("PAID", "Paid")
        PENDING = ("PENDING", "Pending")
        NOT_PAID = ("NOT PAID", "Not paid")

class ContributionOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    donateid = models.CharField(max_length=300, editable=False, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, help_text=_("Enter contribution amount"))
    accepted_laws = models.BooleanField(null=False)
    paid = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="contribution_orders")
    contributor = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, related_name="contribution_orders")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        #generate unique id
        order_id_start = f'#{timezone.now().year}{timezone.now().month}'
        queryset = ContributionOrder.objects.filter(donateid__iexact=order_id_start).count()
      

        count = 1
        donateid = order_id_start
        while(queryset):
            donateid = f'#{timezone.now().year}{timezone.now().month}{count}'
            count += 1
            queryset = ContributionOrder.objects.all().filter(donateid__iexact=donateid).count()
        
        self.donateid = donateid
        
        super(ContributionOrder, self).save(*args, **kwargs)

class TicketOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    ticketorderid = models.CharField(max_length=300, db_index=True, unique=True)
    quantity = models.PositiveBigIntegerField(default=1)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2)
    accepted_laws = models.BooleanField(null=False)
    email = models.EmailField(null=False)
    phone = models.CharField(_("Enter your cellphone number"), max_length=15, validators=[PHONE_REGEX], unique=True)
    buyer = models.ForeignKey(get_user_model(), related_name="ticketorders", null=True, blank=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, related_name="sold_tickets", on_delete=models.CASCADE)
    paid = models.CharField(max_length=300, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        pass

    def save(self, *args, **kwargs):
        order_id_start = f'#{timezone.now().year}{timezone.now().month}'
        queryset = TicketOrder.objects.filter(ticketorderid__iexact=order_id_start).count()

        count = 1
        orderid = order_id_start
        while(queryset):
            orderid = f'#{timezone.now().year}{timezone.now().month}{count}'
            count += 1
            queryset = TicketOrder.objects.all().filter(ticketorderid__iexact=orderid).count()
        self.ticketorderid = orderid

        # Calculate total price
        self.total_price = Decimal(self.quantity) * self.event.ticket_price
        super(TicketOrder, self).save(*args, **kwargs)

    def send_order(self):
        message = f"""
                    Dear {self.event.author.first_name}, \n You have received an order of {self.quantity} ticket(s) for {self.event.title} event from {self.buyer.first_name}.
                """
        print("Hello")