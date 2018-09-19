from model.tweet import Tweet
from services.query_bus import IRequestHandler, IRequest, IResponse
from flask_injector import inject
from services.tweets_repository import TweetsRepository


class UserTweetsRequest(IRequest):
    limit: int
    username: str

    def __init__(self, hashtag: str, limit: int) -> None:
        self.username = hashtag
        self.limit = limit


class UserTweetsResponse(IResponse):
    tweets: [Tweet]

    def __init__(self, tweets: [Tweet]) -> None:
        self.tweets = tweets


class UserTweetsHandler(IRequestHandler):
    _tweetsRepository: TweetsRepository

    @inject
    def __init__(self, tweetsRepository: TweetsRepository):
        self._tweetsRepository = tweetsRepository

    def support(self, request: IRequest) -> bool:
        return isinstance(request, UserTweetsRequest)

    def handle(self, request: UserTweetsRequest) -> UserTweetsResponse:
        return UserTweetsResponse(
            self._tweetsRepository.get_tweets_by_username(request.username, request.limit)
        )
