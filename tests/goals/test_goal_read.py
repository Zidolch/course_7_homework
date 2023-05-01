from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.models import Goal
from tests.factories import UserFactory


@pytest.mark.django_db
class TestGoalRetrieve:
    def test_get_unauthorized(self, client: APIClient) -> None:
        url = reverse('goal_read', args=[1])

        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_goal_as_owner(self, auth_client: APIClient, goal: Goal, user: UserFactory) -> None:
        url = reverse('goal_read', args=[goal.id])
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': goal.id,
            'user': {'email': user.email,
                     'first_name': user.first_name,
                     'id': user.id,
                     'last_name': user.last_name,
                     'username': user.username},
            'category': goal.category.id,
            'created': ANY,
            'updated': ANY,
            'title': goal.title,
            'description': goal.description,
            'due_date': goal.due_date,
            'status': goal.status,
            'priority': goal.priority
        }
