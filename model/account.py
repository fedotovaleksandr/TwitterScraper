from services.json_encoder import IJSONSerializable


class Account(IJSONSerializable):
    fullname: str
    href: str
    id: int

    def __init__(self, id: int, fullname: str, href: str):
        self.id = id
        self.href = href
        self.fullname = fullname

    def to_json(self):
        return self.__dict__
