from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("users/", views.UserListCreateAPIView.as_view(), name="users"),
    path("users/<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user"),
    path("payments/", views.PaymentListCreateAPIView.as_view(), name="payments"),
    path("payments/<int:pk>/", views.PaymentRetrieveUpdateDestroyAPIView.as_view(), name="payment"),
]
