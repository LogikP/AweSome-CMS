import json
import uuid


class User:
    def __init__(self, **kwargs) -> None:
        self.author = kwargs["username"]
        self.title = kwargs["email"]
        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, User):
    #         return NotImplemented

    #     return self.username == other.username and self.email == other.email