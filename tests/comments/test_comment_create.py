from typing import Any
from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from goals.models import Comment, Goal


@pytest.mark.django_db
class TestCommentCreate:
    url = reverse('goal_comment_create')

    def test_create_unauthorized(self, client: APIClient, faker: Any) -> None:
        """
        Неавторизованный пользователь не может создать комментарий
        """
        response = client.post(self.url, data=faker.pydict(1))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_success(self, auth_client: APIClient, goal: Goal) -> None:
        """
        Успешное создание комментария
        """
        response = auth_client.post(self.url, data={
            'text': 'Test comment',
            'goal': goal.id
        })
        comment = Comment.objects.last()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': comment.id,
            'created': ANY,
            'updated': ANY,
            'text': 'Test comment',
            'goal': comment.goal.id
        }