from django.contrib import admin
from campaigns.models import Campaign, Cart, TicketType, IssuedTicket, LiqPayData, TicketCounter, PromoCode
from django.contrib.admin.filters import SimpleListFilter


class NullFilterSpec(SimpleListFilter):
    title = u''

    parameter_name = u''

    def lookups(self, request, model_admin):
        return (
            ('1', 'Has value' ),
            ('0', 'None' ),
        )

    def queryset(self, request, queryset):
        kwargs = {
        '%s'%self.parameter_name : None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class CartNullFilterSpec(NullFilterSpec):
    title = u'Cart'
    parameter_name = u'cart'


class CartInline(admin.StackedInline):
    model = Cart
    extra = 0


class IssuedTicketAdmin(admin.ModelAdmin):
    model = IssuedTicket
    inlines = (CartInline, )
    search_fields = ('cart__name', 'cart__surname', 'uid')
    list_filter = ('cart__ticket_type', )
    readonly_fields = ('timestamp',)


class LiqPayDataInline(admin.StackedInline):
    model = LiqPayData
    extra = 0
    readonly_fields = ('timestamp',)


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_filter = ('status', 'ticket_type', )
    inlines = (LiqPayDataInline,)
    readonly_fields = ('timestamp',)


class LiqPayDataAdmin(admin.ModelAdmin):
    model = LiqPayData
    readonly_fields = ('timestamp',)


class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode
    search_fields = ('cart__name', 'cart__surname', 'uid', 'cart__uid', 'cart__ticket__uid')
    list_filter = ('ticket_type', CartNullFilterSpec)


admin.site.register(Campaign)
admin.site.register(TicketType)
admin.site.register(Cart, CartAdmin)
admin.site.register(IssuedTicket, IssuedTicketAdmin)
admin.site.register(LiqPayData, LiqPayDataAdmin)
admin.site.register(TicketCounter)
admin.site.register(PromoCode, PromoCodeAdmin)
