import unittest
from unittest.mock import patch

from model.tweet import Tweet
from services.query_bus import IRequest
from services.user_handler import UserTweetsHandler, UserTweetsRequest, UserTweetsResponse

expected_username = 'expected'
expected_limit = 123


class UserHandlerTestCase(unittest.TestCase):
    def setUp(self):
        (self.handler, self.repository) = self.create_handler_repository()

    @patch('services.tweets_repository.TweetsRepository')
    def create_handler_repository(self, repository):
        return UserTweetsHandler(repository), repository

    def create_request(self) -> UserTweetsRequest:
        return UserTweetsRequest(expected_username, expected_limit)

    def test_support(self):
        self.assertTrue(self.handler.support(self.create_request()))
        self.assertFalse(self.handler.support(IRequest()))

    def test_handle(self):
        return_val = [Tweet()]
        self.repository.get_tweets_by_username.return_value = return_val
        response = self.handler.handle(self.create_request())
        self.repository.get_tweets_by_username.assert_called_with(expected_username, expected_limit)
        self.assertIsInstance(response, UserTweetsResponse)
        self.assertEqual(response.tweets, return_val)