import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import quote_plus
from requests import Response
from model.tweet import Tweet
from services.tweets_extractor import TweetExtractorResult
from services.tweets_repository import TweetsRepository

expected_hashtag = 'expected_hashtag'
expected_username = 'expected_username'

expected_min_pos = 'expected_min_pos'
expected_limit = 123


class TweetsHandlerTestCase(unittest.TestCase):
    def setUp(self):
        (self.repository, self.client, self.exctractor) = self.create_repository()

    @patch('services.twitter_client.ITwitterClient')
    @patch('services.tweets_extractor.TweetsExtractor')
    def create_repository(self, client, exctractor):
        return TweetsRepository(client, exctractor), client, exctractor

    def test_tweets_by_hashtag_single(self):
        tweets_val = [Tweet()]

        self.client.get.return_value = Response()
        self.exctractor.extract_tweets.return_value = TweetExtractorResult(tweets_val, expected_min_pos)

        result = self.repository.get_tweets_by_hashtag(expected_hashtag, 1)

        self.assertEqual(result, tweets_val)
        self.client.get.assert_called_once()

        firstCall = self.client.get.call_args_list[0]
        self.assertRegex(str(firstCall[0]), '/hashtag/%s' % expected_hashtag)

    def test_tweets_by_hashtag_multiple_limit(self):
        tweet = Tweet()
        tweets_val = [tweet]

        self.client.get.return_value = self.create_tweets_client_response()
        self.exctractor.extract_tweets.return_value = TweetExtractorResult(tweets_val, expected_min_pos)

        result = self.repository.get_tweets_by_hashtag(expected_hashtag, 2)

        self.assertEqual(result, [tweet, tweet])
        self.assertEqual(2, self.client.get.call_count)

        firstCall = self.client.get.call_args_list[0]
        self.assertRegex(str(firstCall[0]), '/hashtag/%s' % expected_hashtag)
        secondCall = self.client.get.call_args_list[1]
        self.assertRegex(str(secondCall[0]), '/i/search/timeline/')
        self.assertEqual(expected_min_pos, secondCall[1]['params']['max_position'])
        self.assertEqual(quote_plus('#%s' % expected_hashtag), secondCall[1]['params']['q'])

    def create_tweets_client_response(self):
        response = Response()
        response.json = MagicMock(
            return_value={'items_html': 'str', 'has_more_items': True, 'min_position': 'expected_min_pos'}
        )
        return response

    def test_tweets_by_username_single(self):
        tweets_val = [Tweet()]

        self.client.get.return_value = Response()
        self.exctractor.extract_tweets.return_value = TweetExtractorResult(tweets_val, expected_min_pos)

        result = self.repository.get_tweets_by_username(expected_username, 1)

        self.assertEqual(result, tweets_val)
        self.client.get.assert_called_once()

        firstCall = self.client.get.call_args_list[0]
        self.assertRegex(str(firstCall[0]), '/%s' % expected_username)

    def test_tweets_by_username_multiple_limit(self):
        tweet = Tweet()
        tweets_val = [tweet]

        self.client.get.return_value = self.create_tweets_client_response()
        self.exctractor.extract_tweets.return_value = TweetExtractorResult(tweets_val, expected_min_pos)

        result = self.repository.get_tweets_by_username(expected_username, 2)

        self.assertEqual(result, [tweet, tweet])
        self.assertEqual(2, self.client.get.call_count)

        firstCall = self.client.get.call_args_list[0]
        self.assertRegex(str(firstCall[0]), '/%s' % expected_username)
        secondCall = self.client.get.call_args_list[1]
        self.assertRegex(str(secondCall[0]), '/i/profiles/show/%s/timeline/tweets' % expected_username)
        self.assertEqual(expected_min_pos, secondCall[1]['params']['max_position'])
