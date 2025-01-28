from rest_framework import serializers

from materials.serializers import PaymentSerializer
from .models import User


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number", "country", "avatar"]


class UserDetailSerializer(serializers.ModelSerializer):
    payments_history = PaymentSerializer(source="payments", many=True)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number",
                  "country", "avatar", "payments_history"]
