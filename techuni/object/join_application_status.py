import os
from enum import Enum, auto
from discord import ForumChannel
from techuni.email import EmailTemplate

class JoinApplicationStatus(Enum):
    RECEIVE = (auto(), EmailTemplate.RECEIVE),
    INVITE = (auto(), EmailTemplate.INVITE),
    REJECT = (auto(), None),

    def __init__(self, args):
        self.id = args[0]
        self._tag_id = None
        self._email_template = args[1]

    def get_tag(self, channel: ForumChannel):
        if channel is None:
            raise ValueError("Channel is not set")

        if self._tag_id is None:
            self._tag_id = int(os.environ.get(f"DISCORD_TAG_APPL_{self.name}"))
            if self._tag_id is None:
                raise ValueError(f"Tag ID({self.name}) is not found")

        return channel.get_tag(self._tag_id)

    def get_email_template(self) -> EmailTemplate:
        if not self.need_send_email():
            raise RuntimeError(f"Email Template is not set in {self.name}.")
        return self._email_template

    def need_send_email(self):
        return self._email_template is not None
