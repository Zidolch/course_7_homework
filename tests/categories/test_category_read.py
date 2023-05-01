from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import Board, GoalCategory
from tests.factories import UserFactory


@pytest.mark.django_db
class TestCategoryRetrieve:
    def test_get_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть доску
        """
        url = reverse('category_read', args=[1])
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_category_as_owner(self, auth_client: APIClient, user: UserFactory, board: tuple[Board, GoalCategory]) -> None:
        """
        Невозможно просмотреть удаленную доску
        """
        board, category = board
        url = reverse('category_read', args=[category.id])
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': category.id,
            'user': {'email': user.email,
                     'first_name': user.first_name,
                     'id': user.id,
                     'last_name': user.last_name,
                     'username': user.username},
            'created': ANY,
            'updated': ANY,
            'title': category.title,
            'is_deleted': category.is_deleted,
            'board': category.board.id
        }