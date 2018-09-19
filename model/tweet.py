import datetime

from model.account import Account
from services.json_encoder import IJSONSerializable


class Tweet(IJSONSerializable):
    account: Account
    date: datetime
    hashtags: [str]
    likes: int
    replies: int
    retweets: int
    text: str

    def toJSON(self):
        return self.__dict__
