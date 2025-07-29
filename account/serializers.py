from rest_framework import serializers

from account.models import Beneficiary, Transaction, TransactionStatus, TransactionType
from users.models import Account

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = ['id', 'name', 'iban']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'iban', 'name', 'balance']

class TransferSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    note = serializers.CharField(max_length=300, required=False, allow_blank=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'note', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, attrs):
        sender = attrs.get('sender')
        receiver = attrs.get('receiver')
        amount = attrs.get('amount')

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver must be different accounts.")

        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        if sender.balance < amount:
            raise serializers.ValidationError("Insufficient funds in sender account.")

        return attrs

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            type=TransactionType.TRANSFER,
            sender=validated_data['sender'],
            receiver=validated_data['receiver'],
            amount=validated_data['amount'],
            note=validated_data.get('note', ''),
            status=TransactionStatus.PENDING
        )
        return transaction
        