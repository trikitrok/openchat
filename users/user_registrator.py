from tests.users.test_registerUser import QueryUserByUserName
from users.register_user_command import RegisterUser
from users.user import User


class DuplicatedUser(ValueError):
    pass


class UserRegistrator(object):
    def __init__(self, query_user_by_username: QueryUserByUserName):
        self.query_user_by_username = query_user_by_username

    def execute(self, command: RegisterUser) -> User:
        if self.query_user_by_username.execute(command.username) is not None:
            raise DuplicatedUser('A user with %s already exists' % command.username)
        return User(username=command.username, password=command.password, about=command.about, ID=command.ID)
