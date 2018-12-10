from unittest import TestCase

from infrastructure.posts.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from users.query_relationships_by_followee_id import QueryRelationshipsByFolloweeID
from posts.query_wall_by_user_id import QueryWallByUserID
from posts.wall_by_user_id import WallByUserID
from tests.fixtures.posts import a_post_by_maria, a_post_by_bob, another_post_by_maria
from tests.fixtures.users import maria, bob_follows_maria, inexistent_user_id
from infrastructure.users.followers_repository_in_memory import InMemoryFollowersRepository
from users.exceptions import UnknownUser
from users.query_user_by_id import QueryUserByID


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = WallByUserID(user_id=maria().ID)
        posts_by_user_id = QueryWallByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), a_post_by_bob(), another_post_by_maria()]),
            QueryRelationshipsByFolloweeID(InMemoryFollowersRepository([bob_follows_maria()]))
        )

        post_list = posts_by_user_id.execute(query)

        assert 3 == len(post_list)
        assert a_post_by_maria() in post_list
        assert a_post_by_bob() in post_list
        assert another_post_by_maria() in post_list

    def test_should_throw_an_exception_if_user_does_not_exist(self):
        query = WallByUserID(user_id=inexistent_user_id())
        posts_by_user_id = QueryWallByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), a_post_by_bob(), another_post_by_maria()]),
            QueryRelationshipsByFolloweeID(InMemoryFollowersRepository([bob_follows_maria()]))
        )
        with self.assertRaises(UnknownUser):
            posts_by_user_id.execute(query)