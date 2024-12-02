from typing import List, Type, TypeVar, Generic
from pydantic import BaseModel, ValidationError
from domain.core.utils.notifier import Notifier, NotificationType

TEntity = TypeVar("TEntity")
TValidator = TypeVar("TValidator", bound=BaseModel)


class BaseService(Generic[TEntity]):
    def __init__(self, notifier: Notifier):
        if notifier is None:
            raise ValueError("Notifier is required.")
        self._notifier = notifier

    async def execute_validation_async(self, validator: Type[TValidator], entity: TEntity) -> List[str]:
        errors = []
        try:
            validator.model_validate(entity)
        except ValidationError as e:
            for error in e.errors():
                error_message = f"Property: {error['loc']} - Error: {error['msg']}"
                self._notifier.handle_message(error_message, NotificationType.ERROR)
                errors.append(error_message)
        return errors

    def handle_exception(self, exception: Exception):
        if exception is None:
            raise ValueError("Exception cannot be None.")
        friendly_message = self._generate_friendly_message(exception)
        self._notifier.handle_message(friendly_message, NotificationType.ERROR)

    def _generate_friendly_message(self, exception: Exception) -> str:
        if isinstance(exception, ValueError):
            return "An invalid value was provided. Please check the input and try again."
        elif isinstance(exception, KeyError):
            return "A required key was missing. Please verify the data and try again."
        elif isinstance(exception, RuntimeError):
            return "An unexpected runtime error occurred. Please try again or contact support."
        return f"An unexpected error occurred: {str(exception)}. Please contact support if the issue persists."
