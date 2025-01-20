from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    course_lessons = LessonSerializer(source="lessons", many=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        """
        Подсчет количества уроков в курсе
        """
        return Lesson.objects.filter(course=obj).count()

    def get_course_lessons(self, obj):
        """
        Список уроков в курсе
        """
        return [lesson.id for lesson in Lesson.objects.filter(course=obj)]


class StaffCourseSerializer(CourseSerializer):
    """
    Сериализатор для модели Course, отображающийся модератору и админу
    """
    lessons_count = serializers.SerializerMethodField()
    course_lessons = LessonSerializer(source="lessons", many=True, read_only=True)