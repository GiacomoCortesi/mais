from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')

class NotFoundException(Exception):
    pass

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: str) -> T:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item_id: str) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
