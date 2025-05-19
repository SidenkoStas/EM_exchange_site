from .models import ExchangeProposal, Ad, Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class AdSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # или другой способ отображения пользователя

    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'category', 'condition', 'user', 'created_at']

class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'status', 'created_at']