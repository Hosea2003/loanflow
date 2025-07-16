from rest_framework import serializers

from users.models import Account, AppUser

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(choices=AppUser.AppUserRoles.choices)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        model = AppUser
        fields = [
            'email', 'username', 'password', 'role', 'first_name', 'last_name', 'phone'
        ]

    def create(self, validated_data:dict):
        password = validated_data.pop("password")
        user =  super().create(validated_data)
        user.set_password(password)
        user.save()
    
        role = validated_data.get("role")
        if role == AppUser.AppUserRoles.CLIENT:
            # generate one default account
            Account.objects.create(
                owner = user
            )
        return user
    
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 'iban', 'name', 'balance'
        ]
    
class DetailsUserSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)
    class Meta:
        model = AppUser
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name', 'accounts'
        ]