from abc import ABC, abstractmethod

class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def users(self):
        pass

    @abstractmethod
    async def save_async(self):
        pass

    @abstractmethod
    async def begin_transaction_async(self):
        pass

    @abstractmethod
    async def commit_transaction_async(self):
        pass

    @abstractmethod
    async def rollback_transaction_async(self):
        pass

    @abstractmethod
    async def dispose(self):
        pass
