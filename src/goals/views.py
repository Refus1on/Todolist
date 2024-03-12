from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goals, GoalComment, Board, BoardParticipant
from goals import serializers
from goals.permissions import BoardPermission, GoalCategoryPermission, IsOwnerOrReadOnly, GoalPermission, \
    GoalCommentsPermission
from goals.serializers import BoardSerializer


class BoardCreateView(CreateAPIView):
    serializer_class = serializers.BoardCreateSerializer
    permission_classes = [BoardPermission]


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goals.objects.filter(category__board=instance).update(
                status=Goals.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermission]
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.BoardListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['title']
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermission]
    serializer_class = serializers.GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    # Включаем возможность фильтрации сортировкой и поиском
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['board']
    # Указываем поля по которым можно проводить сортировку
    ordering_fields = ['title', 'created']
    # Указываем поле для дефолтной сортировки
    ordering = ['title']
    # Указываем поле по которому будет происходить поиск
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False,
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = [GoalCategoryPermission, IsOwnerOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goals.objects.filter(category=instance).update(status=Goals.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    permission_classes = [GoalPermission]
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goals
    permission_classes = [GoalPermission]
    serializer_class = serializers.GoalSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = GoalDateFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goals.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id)
            & Q(category_id=self.request.GET.get('category__in'))
            & ~Q(status=Goals.Status.archived)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goals
    serializer_class = serializers.GoalSerializer
    permission_classes = [GoalPermission, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Goals.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goals.Status.archived)
        )

    def perform_destroy(self, instance: Goals):
        instance.status = Goals.Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [GoalCommentsPermission]


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [GoalCommentsPermission]
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [GoalCommentsPermission, IsOwnerOrReadOnly]
    serializer_class = serializers.GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.select_releted('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )




