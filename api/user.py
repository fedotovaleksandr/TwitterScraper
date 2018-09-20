from flask_injector import inject
from services.query_bus import IQueryBus
from services.user_handler import UserTweetsRequest


class User(object):
    @inject
    def get(self, queryBus: IQueryBus, username: str, limit: int = 30) -> dict:
        request = UserTweetsRequest(username, limit)
        response = queryBus.handle(request)
        return response.tweets, 200


class_instance = User()
