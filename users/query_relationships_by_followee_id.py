from users.followers_repository import FollowersRepository
from users.user_id import UserID


class QueryRelationshipsByFolloweeID(object):
    def __init__(self, relationships_repository: FollowersRepository):
        self.relationships_repository = relationships_repository

    def execute(self, user_id: UserID):
        return self.relationships_repository.by_followee_id(user_id)