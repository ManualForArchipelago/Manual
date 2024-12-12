from abc import ABC, abstractmethod
from collections.abc import Container, Sized, Iterable
from typing import Iterator, Any

from ..Items import ManualItem
from ..Locations import ManualLocation

class CollectionList(ABC, Container, Sized, Iterable):
    @property
    @abstractmethod
    def collection(self) -> list:
        """Define this method in your Collection subclass and return the list that should be used for the other methods."""
        pass

    @abstractmethod
    def __contains__(self, name: str) -> bool:
        """Define this method in your Collection subclass and return a bool for whether the list item's name property matches the passed-in string."""
        pass

    @abstractmethod
    def __getitem__(self, name: str) -> list | dict | ManualItem | ManualLocation:
        """Define this method in your Collection subclass and return the list item(s) whose name property matches the passed-in string."""
        pass

    # def __setitem__ is not compatible with getitem's list result, and dict/ManualItem/ManualLocation are individually settable on their own.

    @abstractmethod
    def __delitem__(self, obj: dict | ManualItem | ManualLocation):
        """Define this method in your Collection subclass and remove the specific dict/object that you pass in.
           (This intentionally does not support a string arg, as the user should __getitem__ or similar first.)"""
        pass

    def __len__(self) -> int:
        return len(self.collection)

    # def __bool__ is not needed because the default behavior in its absence is __len__ > 0, which is what we'd do here anyways

    def __iter__(self) -> Iterator:
        return iter(self.collection)
       
    def filter(self, func) -> list:
        return filter(func, self.collection)

    def each(self, func):
        for i in self.collection:
            i = func(i) or i

    def get(self, criteria: str | dict) -> dict | ManualItem | ManualLocation:
        result = self.__get(criteria)

        if isinstance(result, list):
            # This may need to be a different exception type. Went with TypeError because seemed closest, but could also maybe be KeyError.
            raise TypeError("get() is intended to retrieve a single result, but multiple results were found. Use get_all() instead.")

        return result

    def get_all(self, criteria: str | dict) -> list:
        result = self.__get(criteria)

        if not isinstance(result, list):
            result = [result]

        return result

    def __get(self, criteria: str | dict) -> list | dict | ManualItem | ManualLocation:
        if isinstance(criteria, dict):
            result = []

            for k, v in criteria.items():
                result.append(set([
                    i for i in self.collection if (isinstance(i, dict) and i.get(k) == v) or (getattr(i, k) == v)
                ]))

            result = list(result.intersection(*result))
        else:
            result = self.__getitem__(criteria)

        return result

