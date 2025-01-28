from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from users.models import User

from .models import Lesson


# Create your tests here.
class LessonTestCase(APITestCase):
    """
    Тестирование функционала контроллеров Lesson
    """

    def setUp(self):
        """
        Подготовка исходных данных
        """

        self.user = User.objects.create(email="test@email.com")
        self.moderator = User.objects.create(email="moderator@email.com")
        group = Group.objects.create(name="Moderators")
        self.moderator.groups.add(group)

        self.lesson = Lesson.objects.create(name="Тестовый урок 1",
                                            description="Первый тестовый урок",
                                            owner=self.user)
        self.lesson_2 = Lesson.objects.create(name="Тестовый урок 2", description="Второй тестовый урок")
        self.client.force_authenticate(self.user)

    def test_lesson_retrieve(self):
        """
        Тест просмотра объекта Lesson
        """

        # Обычный пользователь - собственный урок
        url = reverse("materials:lesson", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

        # Обычный пользователь - чужой урок
        url = reverse("materials:lesson", args=[self.lesson_2.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lesson", args=[self.lesson.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """
        Тест создания объекта Lesson и автоматического заполнения поля owner
        """

        # Обычный пользователь
        url = reverse("materials:lessons")
        data = {
            "name": "Тестовый урок 3",
            "description": "Третий тестовый урок"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["owner"], self.user.pk)
        self.assertEqual(Lesson.objects.all().count(), 3)

        # Модератор
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lessons")
        data = {
            "name": "Тестовый урок 3",
            "description": "Третий тестовый урок"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        """
        Тест обновления объекта Lesson и корректного заполнения поля video_link
        """

        # Обычный пользователь - свой урок
        url = reverse("materials:lesson", args=[self.lesson.pk])
        data = {
            "video_link": "https://www.youtube.com/..."
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("video_link"), "https://www.youtube.com/...")

        # Обычный пользователь - чужой урок
        url = reverse("materials:lesson", args=[self.lesson_2.pk])
        data = {
            "video_link": "https://www.youtube.com/..."
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lesson", args=[self.lesson.pk])
        data = {
            "video_link": "https://www.youtube.com"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("video_link"), "https://www.youtube.com")

    def test_invalid_video_link(self):
        """
        Тест некорректного заполнения поля video_link
        """

        url = reverse("materials:lesson", args=[self.lesson.pk])
        data = {
            "video_link": "https://www.google.com/..."
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesRegex(ValidationError, "Ссылка может быть только видео сервис youtube.com")

    def test_lesson_delete(self):
        """
        Тест удаления объекта Lesson
        """

        # Обычный пользователь - свой урок
        url = reverse("materials:lesson", args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)

        # Обычный пользователь - чужой урок
        url = reverse("materials:lesson", args=[self.lesson_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

        # Модератор
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lesson", args=[self.lesson_2.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        """
        Тест вывода списка объектов Lesson
        """

        # Обычный пользователь
        url = reverse("materials:lessons")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results': [{'id': self.lesson.pk,
                               'name': self.lesson.name,
                               'preview': self.lesson.preview,
                               'description': self.lesson.description,
                               'video_link': self.lesson.video_link,
                               'course': None,
                               'owner': self.lesson.owner.pk}]}

        self.assertEqual(data, result)

        # Модератор
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lessons")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = {'count': 2,
                  'next': None,
                  'previous': None,
                  'results': [{'id': self.lesson.pk,
                               'name': self.lesson.name,
                               'preview': self.lesson.preview,
                               'description': self.lesson.description,
                               'video_link': self.lesson.video_link,
                               'course': None,
                               'owner': self.lesson.owner.pk},
                              {'id': self.lesson_2.pk,
                               'name': self.lesson_2.name,
                               'preview': self.lesson_2.preview,
                               'description': self.lesson_2.description,
                               'video_link': self.lesson_2.video_link,
                               'course': None,
                               'owner': None}
                              ]}

        self.assertEqual(data, result)