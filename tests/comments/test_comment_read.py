from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from goals.models import Comment, Goal
from tests.factories import UserFactory


@pytest.mark.django_db
class TestCommentRetrieve:
    def test_retrieve_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть комментарий
        """
        url = reverse('goal_comment_read', args=[1])
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_comment_as_owner(self, auth_client: APIClient, goal: Goal, comment: Comment, user: UserFactory) -> None:
        url = reverse('goal_comment_read', args=[comment.id])
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': comment.id,
            'user': {'email': user.email,
                     'first_name': user.first_name,
                     'id': user.id,
                     'last_name': user.last_name,
                     'username': user.username},
            'created': ANY,
            'updated': ANY,
            'text': comment.text,
            'goal': comment.goal.id
        }