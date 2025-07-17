from rest_framework import serializers

from account.models import Beneficiary
from users.models import Account

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ['id', 'name', 'iban']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'iban', 'name', 'balance']