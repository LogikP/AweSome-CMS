import json
import uuid
from datetime import datetime


class Article:
    def __init__(self, title, tags, author_id, content, **kwargs) -> None:
        self.title = title
        self.tags = tags
        self.author_id = author_id
        self.content = content
        # self.created_at = dateatime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = None

        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Article):
            return NotImplemented

        return self.title == other.title and self.content == other.content
