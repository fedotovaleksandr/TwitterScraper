from datetime import datetime
from flask.json import JSONEncoder
from abc import ABCMeta


class IJSONSerializable:
    __metaclass__ = ABCMeta

    def to_json(self):
        raise NotImplementedError


class ApiJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%I:%M - %d %b %y")
        if isinstance(obj, IJSONSerializable):
            return obj.to_json()

        return super(ApiJSONEncoder, self).default(obj)
