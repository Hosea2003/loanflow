from rest_framework import serializers

from users.models import Account, AppUser

class CreateAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(choices=AppUser.AppUserRoles.choices)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

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