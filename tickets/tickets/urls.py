"""tickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from campaigns.views import CampaignListView, CampaignDetailView, TicketTypeListView, BuyTicketView, CartDetailView, \
    TicketDetailView
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='campaign-list', permanent=False), name='root'),
    url(r'^campaigns/(?P<slug>[-\w]+)/$', CampaignDetailView.as_view(), name='campaign-details'),
    url(r'^campaigns/$', CampaignListView.as_view(), name='campaign-list'),
    url(r'^campaigns/(?P<campaign_slug>[-\w]+)/tickets/$', TicketTypeListView.as_view(),
        name='tickettypes-for-campaign-list'),
    url(r'^campaigns/(?P<campaign_slug>[-\w]+)/tickets/(?P<tickettype_id>\d+)/buy$', BuyTicketView.as_view(),
        name='buy-ticket'),
    url(r'^cart/(?P<slug>[-\w]+)/$', CartDetailView.as_view(), name='cart-details'),
    url(r'^ticket/(?P<slug>[-\w]+)/$', TicketDetailView.as_view(), name='ticket-details'),
]
