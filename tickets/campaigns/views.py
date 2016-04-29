from campaigns.models import Campaign
from django.shortcuts import render
from django.views.generic import ListView, DetailView


class CampaignListView(ListView):
    model = Campaign


class CampaignDetailView(DetailView):
    model = Campaign
