class User(object):
    def get(self, accountId: int) -> dict:
        return {"message": "it is user %s:  tweets response" % accountId }, 200

class_instance = User()