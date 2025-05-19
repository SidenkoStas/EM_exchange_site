from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Ad,  ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdListAPIView(generics.ListAPIView):
    """
    Просмотр списка объявлений с фильтрацией и пагинацией.
    """
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Можно добавить пагинацию DRF

    def get_queryset(self):
        filtering = self.kwargs.get('filtering')
        queryset = Ad.objects.all().order_by('-created_at')
        if filtering:
            try:
                filter_label = Ad.Condition[filtering].label
                queryset = queryset.filter(condition=filter_label)
            except KeyError:
                queryset = queryset.filter(Q(category__title=filtering) | Q(condition=filtering))
        return queryset

class AdDetailAPIView(generics.RetrieveAPIView):
    """
     Просмотр деталей объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

class AdCreateAPIView(generics.CreateAPIView):
    """
    Создание объявления.
    """
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете редактировать это объявление")
        return obj

class AdDeleteAPIView(APIView):
    """
    # Удаление объявления.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        ad = Ad.objects.filter(pk=pk).first()
        if not ad:
            return Response({"detail": "Объявление не найдено"}, status=status.HTTP_404_NOT_FOUND)
        if ad.user != request.user:
            return Response({"detail": "Нет прав на удаление"}, status=status.HTTP_403_FORBIDDEN)
        ad.delete()
        return Response({"detail": "Объявление удалено"}, status=status.HTTP_204_NO_CONTENT)

class ProfileAdsAPIView(generics.ListAPIView):
    """
    Просмотр профиля пользователя - список его объявлений.
    """
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user).order_by('-created_at')

class AdSearchAPIView(generics.ListAPIView):
    """
    Поиск объявлений
    """
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        searching = self.request.query_params.get("searching", "")
        return Ad.objects.annotate(
            lower_title=Lower("title"),
            lower_description=Lower("description")
        ).filter(
            Q(lower_title__icontains=searching.lower()) | Q(lower_description__icontains=searching.lower())
        ).order_by('-created_at')

class ExchangeListAPIView(generics.ListAPIView):
    """
    Просмотр списка обменов пользователя с фильтрацией.
    """
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filt = self.kwargs.get("ex_filter")
        qs = ExchangeProposal.objects.all()
        if filt == "sender":
            qs = qs.filter(ad_sender__user=user)
        elif filt == "receiver":
            qs = qs.filter(ad_receiver__user=user)
        elif filt:
            qs = qs.filter(Q(ad_sender__user=user) | Q(ad_receiver__user=user), status=filt)
        else:
            qs = qs.filter(Q(ad_sender__user=user) | Q(ad_receiver__user=user))
        return qs.order_by('-created_at')

class ExchangeCreateAPIView(generics.CreateAPIView):
    """
    Создание запроса на обмен.
    """
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad_receiver_pk = self.kwargs.get('pk')
        ad_receiver = get_object_or_404(Ad, pk=ad_receiver_pk)
        serializer.save(ad_receiver=ad_receiver)
