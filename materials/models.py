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
