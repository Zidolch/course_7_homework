from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, Comment


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

    def validate_category(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")
        return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    def validate_category(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.exclude(status=Goal.Status.archived)
    )

    def validate_category(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentSerializer(serializers.ModelSerializer):
    def validate_category(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of comment")
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", 'goal')



