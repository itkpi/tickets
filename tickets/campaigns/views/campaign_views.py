import logging

from campaigns.models import Campaign
from django.views.generic import ListView, DetailView

logger = logging.getLogger(__name__)


class CampaignListView(ListView):
    model = Campaign
    queryset = Campaign.objects.filter(opened=True)


class CampaignDetailView(DetailView):
    model = Campaign
