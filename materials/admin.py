from django.contrib import admin
from .models import Course, Lesson
from users.models import Payment



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_date")