from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from materials.models import Payment
from src.utils import get_queryset_for_owner, check_session_status
from .models import User
from .serializers import PaymentSerializer, UserSerializer, NewUserSerializer, UserDetailSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .permissions import IsCurrentUser, IsModerator, IsOwner



class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user == self.get_object():
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT"]:
            self.permission_classes = [IsCurrentUser | IsModerator | IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsCurrentUser | IsAdminUser]
        return super().get_permissions()


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["payment_date"]
    filterset_fields = ["course", "lesson", "payment_method"]

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, self.queryset)

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.owner = self.request.user
        payment.save()


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Дженерик для просмотра, редактирования и удаления объекта Payment:
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        """
        Выдача разрешений в зависимости от статуса пользователя
        """
        if self.request.method == "GET":
            self.permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.request.method in ["PATCH", "PUT", "DELETE"]:
            self.permission_classes = [IsModerator | IsAdminUser]
        return super().get_permissions()

    def get_object(self):
        """
        Уточнение статуса для неоплаченного платежа при обращении к объекту
        """
        payment = super().get_object()
        if payment.session_id and payment.status == "unpaid":
            payment.status = check_session_status(payment.session_id)
            payment.save()
        return payment
