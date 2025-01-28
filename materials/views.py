from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group

from .models import Course, Lesson, Subscription
from .paginators import LessonPaginator, CoursePaginator
from .serializers import CourseSerializer, LessonSerializer, StaffCourseSerializer, SubscriptionSerializer
from src.utils import get_queryset_for_owner
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner | IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, self.queryset)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_class(self):
        try:
            if self.request.user.is_superuser or self.request.user.groups.get(name="Moderators"):
                return StaffCourseSerializer
        except Group.DoesNotExist:
            return CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator


    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [~IsModerator]
        return super().get_permissions()

    def get_queryset(self):
        return get_queryset_for_owner(self.request.user, self.queryset)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT", "GET"]:
            self.permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsOwner | IsAdminUser]
        return super().get_permissions()


class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        """
        Выдача разрешений в зависимости от статуса пользователя
        """
        if self.request.method == "POST":
            self.permission_classes = [IsModerator | IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        """
        Подбор списка объектов в зависимости от статуса пользователя
        """
        return get_queryset_for_owner(self.request.user, self.queryset)


class SubscriptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        """
        Выдача разрешений в зависимости от статуса пользователя
        """
        if self.request.method == "GET":
            self.permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.request.method in ["PATCH", "PUT", "DELETE"]:
            self.permission_classes = [IsModerator | IsAdminUser]
        return super().get_permissions()
