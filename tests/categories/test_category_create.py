from typing import Any
from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.models import GoalCategory, Board


@pytest.mark.django_db
class TestCategoryCreate:
    url = reverse('category_create')

    def test_create_unauthorized(self, client: APIClient, faker: Any) -> None:
        response = client.post(self.url, data=faker.pydict(1))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_success(self, auth_client: APIClient, board: tuple[Board, GoalCategory]) -> None:
        board, _ = board
        response = auth_client.post(self.url, data={
            'title': 'Category',
            'board': board.id
        })
        category = GoalCategory.objects.last()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': category.id,
            'created': ANY,
            'updated': ANY,
            'title': category.title,
            'is_deleted': category.is_deleted,
            'board': category.board.id
        }
