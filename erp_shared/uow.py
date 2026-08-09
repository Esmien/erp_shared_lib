from abc import ABC, abstractmethod
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork(ABC):
    session: AsyncSession | None

    @abstractmethod
    async def __aenter__(self): ...
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    @abstractmethod
    async def commit(self): ...
    @abstractmethod
    async def rollback(self): ...


class BaseUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if exc_type:
            await self.rollback()
        if self.session:
            await self.session.close()

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def rollback(self):
        if self.session:
            await self.session.rollback()
