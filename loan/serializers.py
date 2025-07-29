from rest_framework import serializers

from users.models import AppUser
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
    consultant = serializers.PrimaryKeyRelatedField(
        required=False, 
        allow_null=True, 
        queryset=AppUser.objects.all()
    )

    class Meta:
        model = Loan
        fields = [
            'amount',
            'consultant',
        ]
        extra_kwargs = {
            'consultant': {'required': False, 'allow_null': True},
        }