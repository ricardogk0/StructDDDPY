from typing import List, TypeVar, Generic, Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.core.entities.entity_base import EntityBase
from src.domain.core.interfaces.repositories.i_base_repository import IBaseRepository

TEntity = TypeVar("TEntity", bound=EntityBase)


class BaseRepository(IBaseRepository[TEntity], Generic[TEntity]):
    def __init__(self):
        self._data_store: List[TEntity] = []

    def set_session(self, session: AsyncSession) -> None:
        self._session = session

    def get_by_id(self, entity_id: str) -> Optional[TEntity]:
        return next((entity for entity in self._data_store if entity.id == entity_id), None)

    def get_all(self) -> List[TEntity]:
        return self._data_store

    def add(self, entity: TEntity) -> None:
        self._data_store.append(entity)

    def add_range(self, entities: List[TEntity]) -> None:
        self._data_store.extend(entities)

    def update(self, entity: TEntity) -> None:
        for index, stored_entity in enumerate(self._data_store):
            if stored_entity.id == entity.id:
                self._data_store[index] = entity
                return
        raise ValueError(f"Entity with id {entity.id} not found.")

    def update_range(self, entities: List[TEntity]) -> None:
        for entity in entities:
            self.update(entity)

    def delete(self, entity: TEntity) -> None:
        entity.toggle_is_deleted()
        self.update(entity)

    def delete_range(self, entities: List[TEntity]) -> None:
        for entity in entities:
            self.delete(entity)

    def find(self, predicate: Callable[[TEntity], bool]) -> List[TEntity]:
        return [entity for entity in self._data_store if predicate(entity)]
