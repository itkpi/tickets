from django.contrib import admin
from campaigns.models import Campaign, Cart, TicketType, IssuedTicket, LiqPayData, TicketCounter, PromoCode


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0


class IssuedTicketAdmin(admin.ModelAdmin):
    model = IssuedTicket
    inlines = [CartInline, ]


admin.site.register(Campaign)
admin.site.register(TicketType)
admin.site.register(Cart)
admin.site.register(IssuedTicket, IssuedTicketAdmin)
admin.site.register(LiqPayData)
admin.site.register(TicketCounter)
admin.site.register(PromoCode)
