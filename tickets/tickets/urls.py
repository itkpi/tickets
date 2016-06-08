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
from campaigns.views.api_views import HelloWorld, LiqPayS2S
from campaigns.views.buy_views import CartDetailView
from campaigns.views.campaign_views import CampaignListView, CampaignDetailView
from campaigns.views.issuedticket_views import TicketDetailView, TicketDetailEmailView, TicketDetailPDFView, CheckInView, TicketEmailSendView
from campaigns.views.tickets_views import TicketTypeListView
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='campaign-list', permanent=False), name='root'),
    url(r'^campaigns/(?P<slug>[-\w]+)/$', CampaignDetailView.as_view(), name='campaign-details'),
    url(r'^campaigns/$', CampaignListView.as_view(), name='campaign-list'),
    url(r'^campaigns/(?P<campaign_slug>[-\w]+)/tickets/$', TicketTypeListView.as_view(),
        name='tickettypes-for-campaign-list'),
    url(r'^cart/(?P<slug>[-\w]+)/$', CartDetailView.as_view(), name='cart-details'),
    url(r'^ticket/(?P<slug>[-\w]+)/$', TicketDetailView.as_view(), name='ticket-details'),
    url(r'^ticket/(?P<slug>[-\w]+)/pdf/$', TicketDetailPDFView.as_view(), name='ticket-details-pdf'),
    url(r'^ticket/(?P<slug>[-\w]+)/email/$', TicketDetailEmailView.as_view(), name='ticket-details-email'),
    url(r'^ticket/(?P<slug>[-\w]+)/send-email/$', TicketEmailSendView.as_view(), name='ticket-send-notification'),
    url(r'^event/check-in/$', CheckInView.as_view(), name='check-in'),
    url(r'^event/qr-scan/$', login_required(TemplateView.as_view(template_name='campaigns/qr_scan.html'), login_url='/admin/login/'), name='qr-scan'),

    url(r'^api/v1/hello/$', HelloWorld.as_view(), name='api-hello'),
    url(r'^api/v1/liqpay/$', LiqPayS2S.as_view(), name='api-liqpay'),

    url(r'^report_builder/', include('report_builder.urls'))
]
