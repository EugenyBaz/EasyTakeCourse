import logging

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.log import log_response
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from config import settings
from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serialaizers import CourseSerializer, LessonSerializer
from lms.tasks import send_information_about_update_course
from users.permissions import (IsModer, IsOwner, IsOwnerOrModer, NOTModer,
                               NOTModerOrIsOwner)

logger = logging.getLogger(__name__)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Updated course {instance.pk}. Fetching subscribers...")

        subscriptions = Subscription.objects.filter(course=instance.pk)
        # print(f"Subscriptions count: {subscriptions.count()}")
        if subscriptions.exists():
            emails = list(subscriptions.values_list("user__email", flat=True))
            logger.info(f"Fetching emails: {emails}")
            # print(f"Emails fetched: {emails}")# Берём электронные адреса подписчиков
            send_information_about_update_course.delay(emails)

        # try:
        #     send_mail(
        #         'Test Subject',
        #         'This is a test message.',
        #         settings.DEFAULT_FROM_EMAIL,
        #         ['eugeny.bazavod@list.ru'],  # Сюда подставьте реальный email
        #         fail_silently=False
        #     )
        #     print("Ну, круто получил же письмо!")
        # except Exception as e:
        #     print(f"Ошибка доставки письма: {e}")

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), NOTModer()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), IsOwnerOrModer()]
        elif self.action == "destroy":
            return [IsAuthenticated(), NOTModerOrIsOwner()]
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NOTModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NOTModerOrIsOwner]


class SubscribeUnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, pk=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():  # Если подписка уже существует
            subscription.delete()
            message = "Подписка удалена."
        else:  # Если подписки нет
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена."

        return Response({"message": message}, status=status.HTTP_200_OK)
