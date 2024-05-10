import os
from enum import Enum, auto
from discord import ForumChannel

class JoinApplicationStatus(Enum):
    RECEIVE = auto(),
    INVITE = auto(),
    REJECT = auto(),
    COMPLETE = auto(),

    def __init__(self, _id):
        self.id = _id
        self._tag_id = None

    def get_tag(self, channel: ForumChannel):
        if channel is None:
            raise ValueError("Channel is not set")

        if self._tag_id is None:
            self._tag_id = int(os.environ.get(f"DISCORD_TAG_APPL_{self.name}"))
            if self._tag_id is None:
                raise ValueError(f"Tag ID({self.name}) is not found")

        return channel.get_tag(self._tag_id)
