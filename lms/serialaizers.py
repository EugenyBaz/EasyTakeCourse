from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_link
from users.models import User


class LessonSerializer(ModelSerializer):

    link = serializers.URLField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяем, подписан ли текущий пользователь на курс"""
        user = self.context["request"].user
        if isinstance(user, User):
            return bool(Subscription.objects.filter(user=user, course=obj))
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "preview",
            "description",
            "lesson_count",
            "lessons",
            "owner",
            "is_subscribed",
        ]
