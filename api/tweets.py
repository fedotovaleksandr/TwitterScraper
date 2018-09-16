
class Tweets(object):
    def get(self, hashtag: str) -> dict:
        return {"message": "it is hashtag %s tweets response" % hashtag}, 200

class_instance = Tweets()
