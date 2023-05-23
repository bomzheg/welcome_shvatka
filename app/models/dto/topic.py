from dataclasses import dataclass


@dataclass
class Topic:
    id: int
    user_id: int
    topic_id: int
    start_message_id: int
