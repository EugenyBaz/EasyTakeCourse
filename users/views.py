from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Payment, User
from .permissions import IsOwner, IsOwnerOrModer
from .serializers import (PaymentSerializer, PublicUserSerializer,
                          UserSerializer)
from .services import (create_stripe_price, create_stripe_product,
                       create_stripe_session)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "method"]
    ordering_fields = ["payment_date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("Нельзя смотреть чужой профиль")
        return obj

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PublicUserSerializer  # Публичный сериализатор для GET-запросов
        return UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):

        payment = serializer.save(user=self.request.user)

        if payment.paid_course is None:
            raise ValidationError("Необходимо выбрать курс для оплаты.")

        product_id = create_stripe_product(payment.paid_course.name)
        amount_in_rub = payment.amount
        price = create_stripe_price(product_id, amount_in_rub)
        session_id, payment_link = create_stripe_session(price)
        payment.stripe_payment_id = session_id
        payment.link_payment = payment_link
        payment.save()
