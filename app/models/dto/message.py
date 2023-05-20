from dataclasses import dataclass


@dataclass
class Message:
    id: int
    user_id: int
    user_message_id: int
    forum_message_id: int
    from_admin: bool
