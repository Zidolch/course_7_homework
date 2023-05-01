from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, Comment, Board, BoardParticipant


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", 'is_deleted')
        fields = "__all__"

    def create(self, validated_data: dict) -> Board:
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    role = serializers.ChoiceField(choices=BoardParticipant.Role.choices[1:], required=True)

    class Meta:
        model = BoardParticipant
        read_only_fields = ("id", "created", "updated", 'board')
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict) -> Board:
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=self.context['request'].user).delete()
            BoardParticipant.objects.bulk_create([
                BoardParticipant(
                    user=participant['user'],
                    role=participant['role'],
                    board=instance
                )
                for participant in validated_data.get('participants', [])
            ])

            if title := validated_data.get('title'):
                instance.title = title
                instance.save(update_fields=('title', ))

        return instance

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", 'is_deleted')
        fields = "__all__"


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if not BoardParticipant.objects.filter(
            board_id=value.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user.id
        ).exists():
            raise PermissionDenied
        return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if not BoardParticipant.objects.filter(
            board_id=value.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user.id
        ).exists():
            raise PermissionDenied
        return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.exclude(status=Goal.Status.archived)
    )

    def validate_goal(self, value: Goal) -> Goal:
        if not BoardParticipant.objects.filter(
            board_id=value.category.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user.id
        ).exists():
            raise PermissionDenied
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    def validate_goal(self, value: Goal) -> Goal:
        if not BoardParticipant.objects.filter(
            board_id=value.category.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user.id
        ).exists():
            raise PermissionDenied
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", 'goal')



