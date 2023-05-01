import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from goals.models import Goal
from goals.serializers import CommentSerializer
from tests.factories import CommentFactory


@pytest.mark.django_db
class TestCommentList:
    url = reverse('goal_comment_list')

    def test_get_list_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть список комментариев
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_list(self, auth_client: APIClient, goal: Goal, comment_factory: CommentFactory) -> None:
        """
        Успешный просмотр списка комментариев
        """
        comments = comment_factory.create_batch(2, goal=goal)

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        for comment in CommentSerializer(comments, many=True).data:
            assert comment in response.data
