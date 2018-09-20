import random

import requests
from requests import Response
from abc import ABCMeta, abstractmethod


class ITwitterClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, path: str, params: dict, headers: dict = None) -> Response: raise NotImplementedError


class TwitterClient(ITwitterClient):
    _requestsClient: requests
    _twitterUrl: str

    def __init__(self, requestsClient: requests, twitterUrl: str = 'https://twitter.com'):
        self._twitterUrl = twitterUrl
        self._requestsClient = requestsClient

    def get(self, path: str, params: dict, headers: dict = None) -> Response:
        if headers is None:
            headers = {}
        return self._requestsClient.get(self._twitterUrl + path, headers=headers, params=params)


class TwitterClientHeaderDecorator(ITwitterClient):
    client: ITwitterClient

    userAgents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106
        Safari/537.36''',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    ]

    def __init__(self, client: ITwitterClient):
        self.client = client

    def get(self, path: str, params: dict, headers: dict = None) -> Response:
        if headers is None:
            headers = {}
        return self.client.get(
            path,
            headers={
                'user-agent': random.choice(self.userAgents),
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                **headers
            },
            params=params
        )
