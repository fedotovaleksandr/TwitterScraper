from datetime import datetime
from flask.json import JSONEncoder
from abc import ABCMeta


class IJSONSerializable:
    __metaclass__ = ABCMeta

    def toJSON(self): raise NotImplementedError


class ApiJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%I:%M - %d %b %y")
        if isinstance(obj, IJSONSerializable):
            return obj.toJSON()

        return super(ApiJSONEncoder, self).default(obj)
