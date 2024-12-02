from enum import Enum
from typing import List


class NotificationType(Enum):
    INFORMATION = "Information"
    ERROR = "Error"


class Notification:
    def __init__(self, message: str, type: NotificationType):
        if not message.strip():
            raise ValueError("Message cannot be empty or whitespace.")
        self.message = message
        self.type = type
