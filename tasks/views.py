from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_spectacular.utils import extend_schema

from .models import Task, Category
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    TaskSerializer, CategorySerializer,
)


# ── helpers ──────────────────────────────────────────
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


def index(request):
    return render(request, 'index.html')


# ── Auth Views ────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'user':   UserSerializer(user).data,
                'tokens': tokens,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if not user:
                return Response(
                    {'error': 'اسم المستخدم أو كلمة السر غلط'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            tokens = get_tokens_for_user(user)
            return Response({
                'user':   UserSerializer(user).data,
                'tokens': tokens,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (KeyError, TokenError):
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ── Category ViewSet ──────────────────────────────────
@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class   = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ── Task ViewSet ──────────────────────────────────────
@extend_schema(tags=['Tasks'])
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class   = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields   = ['status', 'priority', 'category']
    search_fields      = ['title', 'description']
    ordering_fields    = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.last_completed and (timezone.now() - task.last_completed) < timedelta(hours=14):
            return Response({'error': 'انتظر '}, status=status.HTTP_400_BAD_REQUEST)
        task.last_completed   = timezone.now()
        task.completed_count += 1
        task.save()
        return Response({'status': 'success'})