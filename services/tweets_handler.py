from model.tweet import Tweet
from services.query_bus import IRequestHandler, IRequest, IResponse
from flask_injector import inject

from services.tweets_repository import TweetsRepository


class TweetsRequest(IRequest):
    limit: int
    hashtag: str

    def __init__(self, hashtag: str, limit: int) -> None:
        self.hashtag = hashtag
        self.limit = limit


class TweetsResponse(IResponse):
    tweets: [Tweet]

    def __init__(self, tweets: [Tweet]) -> None:
        self.tweets = tweets


class TweetsHandler(IRequestHandler):
    _tweetsRepository: TweetsRepository

    @inject
    def __init__(self, tweetsRepository: TweetsRepository):
        self._tweetsRepository = tweetsRepository

    def support(self, request: IRequest) -> bool:
        return isinstance(request, TweetsRequest)

    def handle(self, request: TweetsRequest) -> TweetsResponse:
        return TweetsResponse(
            self._tweetsRepository.get_tweets_by_hashtag(request.hashtag, request.limit)
        )
