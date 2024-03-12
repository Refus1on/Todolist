from django.db import models
from django.utils import timezone

from core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class BoardParticipant(BaseModel):
    class Meta:
        # Этой строчкой мы указываем что у одной доски не будет несколько одинаковых пользователей
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants")
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.owner)


class GoalCategory(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название")
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Goals(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, blank=True, on_delete=models.CASCADE, verbose_name="Категория",
                                 related_name='goals')
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name='Статус')
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.low,
                                                verbose_name='Приоритет')
    due_date = models.DateTimeField(verbose_name='Дата дедлайна', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор', related_name='goals')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComment(BaseModel):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE, verbose_name="Цель", related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    text = models.TextField(verbose_name="комментарий")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text

