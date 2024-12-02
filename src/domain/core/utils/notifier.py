from typing import List, Optional
from .notification import Notification, NotificationType


class Notifier:
    def __init__(self):
        self._notifications: List[Notification] = []

    def get_notifications(self) -> List[Notification]:
        return self._notifications

    def has_notification(self) -> bool:
        return len(self._notifications) > 0

    def handle(self, notification: Notification):
        if notification is None:
            raise ValueError("Notification cannot be None.")
        self._notifications.append(notification)

    def handle_message(self, message: str, type: Optional[NotificationType] = NotificationType.INFORMATION):
        if not message.strip():
            raise ValueError("Message cannot be empty or whitespace.")
        self._notifications.append(Notification(message, type))

    def handle_exception(self, exception: Exception):
        if exception is None:
            raise ValueError("Exception cannot be None.")
        friendly_message = self._generate_friendly_message(exception)
        self._notifications.append(Notification(friendly_message, NotificationType.ERROR))

    def _generate_friendly_message(self, exception: Exception) -> str:
        if isinstance(exception, ValueError):
            return "An invalid value was provided. Please check the input and try again."
        elif isinstance(exception, KeyError):
            return "A required key was missing. Please verify the data and try again."
        elif isinstance(exception, RuntimeError):
            return "An unexpected runtime error occurred. Please try again or contact support."
        return f"An unexpected error occurred: {str(exception)}. Please contact support if the issue persists."

    def notify_validation_errors(self, validation_errors: List[str]):
        for error in validation_errors:
            self._notifications.append(Notification(error, NotificationType.ERROR))

    def clean(self):
        self._notifications.clear()
