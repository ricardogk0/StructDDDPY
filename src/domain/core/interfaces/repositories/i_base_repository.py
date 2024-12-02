from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Callable

TEntity = TypeVar("TEntity")


class IBaseRepository(ABC, Generic[TEntity]):
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[TEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[TEntity]:
        pass

    @abstractmethod
    def add(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    def add_range(self, entities: List[TEntity]) -> None:
        pass

    @abstractmethod
    def update(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    def update_range(self, entities: List[TEntity]) -> None:
        pass

    @abstractmethod
    def delete(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    def delete_range(self, entities: List[TEntity]) -> None:
        pass

    @abstractmethod
    def find(self, predicate: Callable[[TEntity], bool]) -> List[TEntity]:
        pass
