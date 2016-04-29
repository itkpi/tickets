from django.contrib import admin
from campaigns.models import Campaign, Cart, TicketType, IssuedTicket

admin.site.register(Campaign)
admin.site.register(TicketType)
admin.site.register(Cart)
admin.site.register(IssuedTicket)
