from django.contrib import admin
from campaigns.models import Campaign, Cart, TicketType, IssuedTicket, LiqPayData, TicketCounter, PromoCode


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0


class IssuedTicketAdmin(admin.ModelAdmin):
    model = IssuedTicket
    inlines = (CartInline, )
    search_fields = ('cart__name', 'cart__surname', 'uid')
    list_filter = ('cart__ticket_type', )


class LiqPayDataInline(admin.StackedInline):
    model = LiqPayData
    extra = 0


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_filter = ('status', 'ticket_type', )
    inlines = (LiqPayDataInline,)


admin.site.register(Campaign)
admin.site.register(TicketType)
admin.site.register(Cart, CartAdmin)
admin.site.register(IssuedTicket, IssuedTicketAdmin)
admin.site.register(LiqPayData)
admin.site.register(TicketCounter)
admin.site.register(PromoCode)
