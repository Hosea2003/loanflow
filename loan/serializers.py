from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id',
            'consultant',
            'amount',
            'status',
            'date_created',
            'date_assigned',
        ]
        read_only_fields = ['id', 'status', 'date_created', 'date_assigned']

class LoanCreateSerializer(serializers.ModelSerializer):
    consultant = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=None)

    class Meta:
        model = Loan
        fields = [
            'amount',
            'consultant',
        ]
        extra_kwargs = {
            'consultant': {'required': False, 'allow_null': True},
        }