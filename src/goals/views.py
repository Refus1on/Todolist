from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from goals.models import GoalCategory, Goals, GoalComment
from goals import serializers


class CategoryCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CategoryCreateSerializer


class CategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CategorySerializer
    pagination_class = LimitOffsetPagination
    # Включаем возможность фильтрации сортировкой и поиском
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    # Указываем поля по которым можно проводить сортировку
    ordering_fields = ['title', 'created']
    # Указываем поле для дефолтной сортировки
    ordering = ['title']
    # Указываем поле по которому будет происходить поиск
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class CategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_filds=('is_deleted', ))
        return instance


class GoalCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goals
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goals.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goals.Status.archived)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goals
    serializer_class = serializers.GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goals.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goals.Status.archived)
        )


class GoalCommentCreateView(CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)

