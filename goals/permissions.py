from typing import Any

from rest_framework import permissions
from rest_framework.request import Request

from goals.models import BoardParticipant, Goal, Board, GoalCategory, Comment


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: Any, obj: Board) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: Any, obj: GoalCategory) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: Any, obj: Goal) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: Any, obj: Comment) -> bool:
        return request.method in permissions.SAFE_METHODS or BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()
