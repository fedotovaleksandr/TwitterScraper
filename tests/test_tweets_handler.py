import unittest
from unittest.mock import patch

from model.tweet import Tweet
from services.query_bus import IRequest
from services.tweets_handler import TweetsHandler, TweetsRequest, TweetsResponse

expected_hashtag = 'expected'
expected_limit = 123


class TweetsHandlerTestCase(unittest.TestCase):
    def setUp(self):
        (self.handler, self.repository) = self.create_handler_repository()

    @patch('services.tweets_repository.TweetsRepository')
    def create_handler_repository(self, repository):
        return TweetsHandler(repository), repository

    def create_request(self) -> TweetsRequest:
        return TweetsRequest(expected_hashtag, expected_limit)

    def test_support(self):
        self.assertTrue(self.handler.support(self.create_request()))
        self.assertFalse(self.handler.support(IRequest()))

    def test_handle(self):
        return_val = [Tweet()]
        self.repository.get_tweets_by_hashtag.return_value = return_val
        response = self.handler.handle(self.create_request())
        self.repository.get_tweets_by_hashtag.assert_called_with(expected_hashtag, expected_limit)
        self.assertIsInstance(response, TweetsResponse)
        self.assertEqual(response.tweets, return_val)
