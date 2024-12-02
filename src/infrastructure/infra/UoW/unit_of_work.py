from abc import ABC
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncTransaction
from sqlalchemy.orm import sessionmaker
from src.domain.core.interfaces.UoW.i_unit_of_work import IUnitOfWork
from src.infrastructure.infra.repositories.user_repository import UserRepository


class UnitOfWork(IUnitOfWork, ABC):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self._transaction: Optional[AsyncTransaction] = None
        self._session: Optional[AsyncSession] = None
        self._users = UserRepository()

    @property
    def users(self):
        if self._session is None:
            raise RuntimeError("Session not initialized. Use UnitOfWork as a context manager.")
        self._users.set_session(self._session)
        return self._users

    async def __aenter__(self):
        self._session = self._session_factory()
        self._users.set_session(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.dispose()

    async def save_async(self):
        if self._session is not None:
            await self._session.commit()

    async def begin_transaction_async(self):
        if self._transaction is None and self._session is not None:
            self._transaction = await self._session.begin()

    async def commit_transaction_async(self):
        try:
            if self._transaction is not None:
                await self._transaction.commit()
                await self._transaction.close()
                self._transaction = None
        except Exception:
            await self.rollback_transaction_async()
            raise

    async def rollback_transaction_async(self):
        if self._transaction is not None:
            await self._transaction.rollback()
            await self._transaction.close()
            self._transaction = None

    async def dispose(self):
        if self._session is not None:
            await self._session.close()
            self._session = None
        if self._transaction is not None:
            await self._transaction.close()
            self._transaction = None
