from re import *
from typing import Protocol, TypeVar, Callable, DefaultDict
from collections import defaultdict

T = TypeVar("T")
U = TypeVar("U")

class Reader(Protocol[T]):
    def read(self) -> T: ...

class DefaultReader:
    def read(self) -> list[tuple[str, str]]:
        with open('码表.txt') as f:
            text = f.read()
            result: list[tuple[str, str]] = []
            for 行 in findall(r'^(.+)\t(.+)$', text, flags=M):
                result.append((行[0], 行[1]))
            return result

class Processor(Protocol[T, U]):
    def process(self, input: T, freq: dict[str, int], short_dict: dict[str, int]) -> U: ...
    # sort_dict 简码级数

class DefaultProcessor:
    def __init__(self, shorter: Callable[[str], str]):
        self.shorter = shorter
        pass

    def process(self, input: list[tuple[str, str]], freq: dict[str, int], short_dict: dict[str, int]) -> list[tuple[str, str, int]]:
        反码表: DefaultDict[str, list[tuple[str, str]]] = defaultdict(list)
        for entry in input:
            反码表[self.shorter(entry[1])].append(entry)
        result: list[tuple[str, str, int]] = []
        for entry in 反码表.values():
            entry = sorted(entry, key=lambda x: short_dict.get(x[0], len(x[1])))
            频率们 = [freq.get(x[0], 0) for x in entry]
            频率们 = sorted(频率们, reverse=True)
            for entry2, freq2 in zip(entry, 频率们):
                result.append((entry2[0], entry2[1], freq2))
        return result

def default_to_string(input: list[tuple[str, str, int]]) -> str:
    return '\n'.join(
        [f'{entry[0]}\t{entry[1]}\t{entry[2]}' for entry in input]
    )

if __name__ == '__main__':
    reader: Reader[list[tuple[str, str]]] = DefaultReader()
    processor: Processor[list[tuple[str, str]], list[tuple[str, str, int]]] = DefaultProcessor(lambda x: x)
    freq: dict[str, int] = {}
    with open('频率.txt') as f:
        text = f.read()
    for 行 in findall(r'^(.+)\t(\d+)$', text, flags=M):
        freq[行[0]] = int(行[1])
    
    short_dict: dict[str, int] = {}
    try:
        with open('简码级数.txt') as f:
            text = f.read()
            for 行 in findall(r'^(.+)\t(\d)$', text, flags=M):
                short_dict[行[0]] = int(行[1])
    except:
        pass
    
    with open('output.txt', 'w') as f:
        f.write(
            default_to_string(
                processor.process(
                    reader.read(),
                    freq,
                    short_dict
                )
            )
        )
