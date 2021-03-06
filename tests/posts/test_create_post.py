from unittest import TestCase

from domain.posts.create_post_command import CreatePost
from domain.posts.exceptions import UnkownUserID
from domain.posts.post_creator import PostCreator
from domain.posts.post_id import PostID
from domain.users.query_user_by_id import QueryUserByID
from domain.users.user_id import UserID
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria


class TestCreatePost(TestCase):
    def test_should_create_a_post(self):
        command = CreatePost(post_id=PostID(), user_id=maria().ID, text='', created_at=a_perfect_day_and_time())
        post_creator = PostCreator(QueryUserByID(InMemoryUsersRepository([maria()])))

        created_post, events = post_creator.execute(command)

        assert command.post_id == created_post.post_id
        assert command.user_id == created_post.user_id
        assert command.text == created_post.text
        assert command.created_at == created_post.created_at
        assert 1 == len(events)
        assert command.post_id == events[0].post_id
        assert command.user_id == events[0].user_id
        assert command.text == events[0].text
        assert command.created_at == events[0].created_at

    def test_should_throw_an_exception_on_inexistent_user(self):
        command = CreatePost(post_id=PostID(),
                             user_id=UserID('fc673127-c5b9-4128-9015-2bbc31163df1'),
                             text='',
                             created_at=a_perfect_day_and_time())

        post_creator = PostCreator(QueryUserByID(InMemoryUsersRepository([maria()])))

        with self.assertRaises(UnkownUserID):
            post_creator.execute(command)
