from typing import Callable
from urllib.parse import quote_plus
from connexion import ProblemException
from requests import Response
from model.tweet import Tweet
from services.tweets_extractor import TweetsExtractor
from services.twitter_client import ITwitterClient
from flask_injector import inject


class EntityNotFoundException(ProblemException):
    def __init__(self, **kwargs):
        err = 'Entity not found.'
        ProblemException.__init__(self, **kwargs, title=err, detail=err, status=404)


class TwitterUnavailableFoundException(ProblemException):
    def __init__(self, **kwargs):
        err = 'Twitter unavailable.'
        ProblemException.__init__(self, **kwargs, title=err, detail=err, status=500)


class TweetsRepository:
    _client: ITwitterClient

    @inject
    def __init__(self, client: ITwitterClient, extractor: TweetsExtractor):
        self._extractor = extractor
        self._client = client

    def check_response(self, response: Response):
        if response.status_code == 404:
            raise EntityNotFoundException()
        if response.status_code > 500:
            raise TwitterUnavailableFoundException()

    def get_tweets_by_hashtag(self, hashtag: str, limit: int) -> [Tweet]:
        response = self._client.get(
            '/hashtag/{}'.format(quote_plus(hashtag)),
            params={'f': 'tweets', 'src': 'typd'},

        )
        self.check_response(response)
        ext_result = self._extractor.extract_tweets(response.text, limit)
        tweets = ext_result.tweets

        if len(tweets) < limit:
            loaded_tweets = self._load_tweets_by_hashtag(ext_result.min_position, hashtag, limit - len(tweets))
            tweets.extend(loaded_tweets)

        return tweets

    def _load_tweets_by_hashtag(self, min_position: str, hashtag: str, limit: int) -> [Tweet]:
        def request_func(next_position: str) -> Response:
            return self._client.get(
                '/i/search/timeline/',
                params={
                    'vertical': 'default',
                    'q': quote_plus('#' + hashtag),
                    'include_available_features': 1,
                    'include_entities': 1,
                    'max_position': next_position
                },
                headers={
                    'x-requested-with': 'XMLHttpRequest'
                }
            )

        return self._load_tweets_ajax(request_func, min_position, limit)

    def _load_tweets_ajax(self, request_func: Callable[[str], Response], min_position: str, limit: int) -> [Tweet]:
        tweets = []
        next_position = min_position
        while len(tweets) < limit:
            try:
                response = request_func(next_position)
                content = response.json()
            except Exception as e:
                return tweets

            html = content["items_html"]
            new_tweets = self._extractor.extract_tweets(html, limit, False).tweets
            tweets.extend(new_tweets)

            if not content["has_more_items"] and not content["min_position"] or len(new_tweets) == 0:
                return tweets

            next_position = content["min_position"]

        return tweets

    def get_tweets_by_username(self, username: str, limit: int) -> [Tweet]:
        response = self._client.get(
            '/%s' % quote_plus(username),
            params={},
        )
        self.check_response(response)
        ext_result = self._extractor.extract_tweets(response.text, limit)
        tweets = ext_result.tweets

        if len(tweets) < limit:
            loaded_tweets = self._load_tweets_by_username(ext_result.min_position, username, limit - len(tweets))
            tweets.extend(loaded_tweets)

        return tweets

    def _load_tweets_by_username(self, min_position: str, username: str, limit: int) -> [Tweet]:
        def request_func(next_position: str) -> Response:
            return self._client.get(
                '/i/profiles/show/{}/timeline/tweets'.format(quote_plus(username)),
                params={
                    'vertical': 'default',
                    'reset_error_state': 'false',
                    'include_available_features': 1,
                    'include_entities': 1,
                    'max_position': next_position
                },
                headers={
                    'x-requested-with': 'XMLHttpRequest'
                }
            )

        return self._load_tweets_ajax(request_func, min_position, limit)
