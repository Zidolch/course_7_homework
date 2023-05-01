from unittest.mock import ANY
import pytest
from django.urls import reverse
from rest_framework import status
from goals.models import BoardParticipant, Board, GoalCategory
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.mark.django_db
class TestBoardRetrieve:
    def test_retrieve_unauthorized(self, client: APIClient) -> None:
        """
        Не авторизированный пользователь не может просмотреть доску
        """
        url = reverse('board_read', args=[1])
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deleted_board(self, auth_client: APIClient, board: tuple[Board, GoalCategory]) -> None:
        """
        Невозможно просмотреть удаленную доску
        """
        board, _ = board
        board.is_deleted = True
        board.save()

        url = reverse('board_read', args=[board.id])

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_board_as_owner(self, auth_client: APIClient, board: tuple[Board, GoalCategory], user: UserFactory) -> None:
        """
        Успешный просмотр собственной доски
        """
        board, _ = board
        url = reverse('board_read', args=[board.id])

        participant = board.participants.last()

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert participant.user == user
        assert response.json() == {
            'id': board.id,
            'created': ANY,
            'updated': ANY,
            'title': board.title,
            'is_deleted': board.is_deleted,
            'participants': [{
                'id': participant.id,
                'role': BoardParticipant.Role.owner.value,
                'user': user.username,
                'created': ANY,
                'updated': ANY,
                'board': participant.board_id
            }]
        }