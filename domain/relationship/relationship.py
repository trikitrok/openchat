from dataclasses import dataclass

from domain.users.user_id import UserID


@dataclass(frozen=True)
class Relationship:
    followee_id: UserID
    follower_id: UserID
