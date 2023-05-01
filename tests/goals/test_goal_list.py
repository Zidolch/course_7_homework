import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import Board, GoalCategory
from goals.serializers import GoalSerializer
from tests.factories import GoalFactory


@pytest.mark.django_db
class TestGoalsList:
    url = reverse('goal_list')

    def test_get_list_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть список целей
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list_success(self, auth_client: APIClient, board: tuple[Board, GoalCategory], goal_factory: GoalFactory) -> None:
        """
        Успешный просмотр списка целей
        """
        _, category = board
        goals = goal_factory.create_batch(2, category=category)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for cat in GoalSerializer(goals, many=True).data:
            assert cat in response.data
