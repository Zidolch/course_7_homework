import pytest
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, GoalCategory, Goal, Comment
from tests.factories import BoardFactory, CategoryFactory, UserFactory, GoalFactory, CommentFactory

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client: APIClient, user: User) -> APIClient:
    client.force_login(user)
    return client


# @pytest.fixture(autouse=True)
# def another_user(user_factory):
#     return user_factory.create()


@pytest.fixture
def board(board_factory: BoardFactory, category_factory: CategoryFactory, user: UserFactory) -> tuple[Board, GoalCategory]:
    board = board_factory.create(with_owner=user)
    category = category_factory.create(board=board, user=user)
    return board, category


@pytest.fixture
def goal(goal_factory: GoalFactory, user: UserFactory, board: tuple[Board, GoalCategory]) -> Goal:
    _, category = board
    return goal_factory.create(user=user, category=category)


@pytest.fixture
def comment(user: UserFactory, goal: GoalFactory, comment_factory: CommentFactory) -> Comment:
    return comment_factory.create(user=user, goal=goal)

# @pytest.fixture
# def alien_board(board_factory, another_user, category_factory) -> tuple[Board, GoalCategory]:
#     board = board_factory.create(with_owner=another_user)
#     category = category_factory.create(board=board, user=another_user)
#     return board, category
#
#
# @pytest.fixture
# def alien_board_writer(board_factory, board_participant_factory, category_factory, user) -> tuple[Board, GoalCategory]:
#     board = board_factory.create()
#     board_participant_factory(board=board, user=user, role=2)
#     category = category_factory.create(board=board, user=user)
#     return board, category
#
#
# @pytest.fixture
# def alien_board_reader(
#         board_factory, board_participant_factory,
#         category_factory, another_user, user) -> tuple[Board, GoalCategory]:
#     board = board_factory.create()
#     board_participant_factory(board=board, user=user, role=3)
#     category = category_factory.create(board=board, user=another_user)
#     return board, category
