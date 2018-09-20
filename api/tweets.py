from flask_injector import inject
from services.query_bus import IQueryBus
from services.tweets_handler import TweetsRequest


class Tweets(object):
    @inject
    def get(self, queryBus: IQueryBus, hashtag: str, limit: int = 30) -> tuple:
        request = TweetsRequest(hashtag, limit)
        response = queryBus.handle(request)
        return response.tweets, 200


class_instance = Tweets()
