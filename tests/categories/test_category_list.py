import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import Board, GoalCategory
from goals.serializers import GoalCategorySerializer
from tests.factories import CategoryFactory


@pytest.mark.django_db
class TestCategoryList:
    url = reverse('category_list')

    def test_get_list_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть список категорий
        """
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list(self, auth_client: APIClient, board: tuple[Board, GoalCategory], category_factory: CategoryFactory) -> None:
        """
        Успешный просмотр списка категорий
        """
        board, category = board
        categories = category_factory.create_batch(2, board=board)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for cat in GoalCategorySerializer(categories, many=True).data:
            assert cat in response.data

