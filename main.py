from re import *
from typing import Protocol, TypeVar

T = TypeVar("T")

class Reader(Protocol[T]):
    def read(self) -> T: ...

class DefaultReader:
    def read(self) -> list[tuple[str, str]]:
        with open('码表.txt') as f:
            text = f.read()
            result: list[tuple[str, str]] = []
            for 行 in findall(r'^(.+)\t(.+)$', text, flags=M):
                result.append((行[1], 行[2]))
                return result
