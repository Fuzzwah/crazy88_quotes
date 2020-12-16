from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from quotes.models import (
    Quotes
)

class QuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotes
        fields = ['id', 'text']
