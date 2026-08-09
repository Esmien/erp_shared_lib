from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

from erp_shared.uow import IUnitOfWork

DTOType = TypeVar("DTOType", bound=BaseModel)


class BaseService[DTOType: BaseModel](ABC):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @property
    @abstractmethod
    def not_found_exception(self) -> Exception: ...

    async def get_or_raise(self, obj_id: int) -> DTOType:
        # Репозиторий мы опишем абстрактно, он придет из UoW
        obj = await self.repository.get_by_id(obj_id=obj_id)
        if not obj:
            raise self.not_found_exception
        return obj

    async def get(self, obj_id: int) -> DTOType:
        return await self.get_or_raise(obj_id=obj_id)

    async def create(self, create_data: dict[str, Any]) -> DTOType:
        obj = await self.repository.create(**create_data)
        await self.uow.commit()
        return obj

    async def update(self, obj_id: int, update_data: dict[str, Any]) -> DTOType:
        updated_obj = await self.repository.update(obj_id=obj_id, update_data=update_data)
        if not updated_obj:
            raise self.not_found_exception
        await self.uow.commit()
        return updated_obj

    async def delete(self, obj_id: int) -> None:
        await self.repository.delete(obj_id=obj_id)
        await self.uow.commit()
