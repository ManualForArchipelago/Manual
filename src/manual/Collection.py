from abc import ABC, abstractmethod
from collections.abc import Container, Sized, Iterable
from typing import Iterator, Any

from BaseClasses import Region
from Options import Option

class Collection(ABC, Container, Sized, Iterable):
    @property
    @abstractmethod
    def collection(self) -> dict:
        """Define this method in your Collection subclass and return the dict that should be used for the other methods."""
        pass

    @abstractmethod
    def __contains__(self, name: str) -> bool:
        """Define this method in your Collection subclass and return a bool for whether the dict item's name property matches the passed-in string."""
        pass

    @abstractmethod
    def __getitem__(self, name: str) -> list | dict | Option | Region:
        """Define this method in your Collection subclass and return the dict item(s) whose name property matches the passed-in string."""
        pass

    @abstractmethod
    def __setitem__(self, name: str):
        """Define this method in your Collection subclass and set the named value appropriately."""
        pass

    @abstractmethod
    def __delitem__(self, key: str):
        """Define this method in your Collection subclass and delete the named value appropriately."""
        pass

    def __len__(self) -> int:
        # self.collection has to be a dict, so we can still automatically do len of keys from that
        return len(self.collection.keys())

    # def __bool__ is not needed because the default behavior in its absence is __len__ > 0, which is what we'd do here anyways

    def __iter__(self) -> Iterator:
        return iter(self.collection)
       
    def filter(self, func) -> dict:
        return filter(func, self.collection)

    def each(self, func):
        for i in self.collection.values():
            i = func(i) or i

    def get(self, criteria: str | dict) -> dict | Option | Region:
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

    def __get(self, criteria: str | dict) -> list | dict | Option | Region:
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

