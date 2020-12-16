from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from quotes.models import (
    Quote
)

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'text']
