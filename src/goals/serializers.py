from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import UserLoginSerializer, UserRetrieveUpdateSerializer
from goals.models import GoalCategory, Goals, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

    def validate_board(self, value: Board):
        if value.is_deleted:
            raise serializers.ValidationError('Not allowed to delete category.')
        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context['request'].user
        ).exists():
            raise serializers.ValidationError('You must be owner or writer')
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goals
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed category")
        if value.user != self.context["request"].user:
            raise PermissionDenied

        if not BoardParticipant.objects.filter(
            board_id=value.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user
        ).exists():
            raise PermissionDenied
        return value

    # def create(self, validated_data):
    #     user = validated_data["user"]
    #     category = validated_data["category"]
    #     board = category.board
    #     participant = BoardParticipant.objects.filter(board=board, user=user).first()
    #     if not participant:
    #         raise PermissionDenied
    #     if participant.role == BoardParticipant.Role.reader:
    #         raise PermissionDenied
    #     goal = Goals.objects.create(**validated_data)
    #
    #     return goal


class GoalSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goals
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed category")
        if value.user != self.context["request"].user:
            raise PermissionDenied

        return value


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("created", "id", "updated", "user")


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            if title := validated_data.get('title'):
                instance.title = title
                instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
