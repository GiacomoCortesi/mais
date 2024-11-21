from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from models.id import ID

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: ID) -> T:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item_id: ID) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
