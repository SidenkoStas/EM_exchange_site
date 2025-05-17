from rest_framework.generics import ListAPIView
from . import serializers
from .models import Ad, ExchangeProposal
from django.db.models import Q

class AdListApiView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdSerializer

class ExchangeListApiView(ListAPIView):
    serializer_class = serializers.ExchangeProposalSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) |
            Q(ad_receiver__user=user)
        )
        return queryset