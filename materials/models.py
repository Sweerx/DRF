from django.contrib.auth import get_user_model
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="materials/courses/previews/", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="materials/courses/previews/", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    video_link = models.TextField(verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="Курс", null=True, blank=True,
                               related_name="lessons")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    is_active = models.BooleanField(verbose_name="Активна", default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь",
                              related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="subscriptions")
    created_at = models.DateField(verbose_name="Дата активации", auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"Подписка пользователя {self.owner.name} на курс {self.course.name} от {self.created_at}"
