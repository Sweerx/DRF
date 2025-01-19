from rest_framework import serializers

from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
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
