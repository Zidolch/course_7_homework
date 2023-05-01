from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.models import Goal, Board, GoalCategory


@pytest.mark.django_db
class TestGoalCreate:
    url = reverse('goal_create')

    def test_create_unauthorized(self, client: APIClient) -> None:
        """
        Неавторизованный пользователь не может создать цель
        """
        response = client.post(self.url, data={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_success(self, auth_client: APIClient, board: tuple[Board, GoalCategory]) -> None:
        """
        Успешное создание цели
        """
        board, category = board
        response = auth_client.post(self.url, data={
            'category': category.id,
            'title': 'Test title'
        })

        goal = Goal.objects.last()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': goal.id,
            'category': category.id,
            'created': ANY,
            'updated': ANY,
            'title': 'Test title',
            'description': goal.description,
            'due_date': goal.due_date,
            'status': goal.status,
            'priority': goal.priority
        }
