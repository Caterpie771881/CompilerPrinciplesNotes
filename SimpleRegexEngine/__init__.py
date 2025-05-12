from .compiler import *
from typing import Union


def match(regex: str, string: str) -> bool:
    return compile(regex).match(string)


def find(regex: str, string: str) -> Union[str, None]:
    return compile(regex).find(string)


def findall(regex: str, string: str) -> list[str]:
    return compile(regex).findall(string)
    

def split(
        regex: str,
        string: str,
        maxsplit: int = 0
    ) -> list[str]:
    return compile(regex).split(string, maxsplit)


def sub(
        regex: str,
        repl: str,
        string: str,
        count: int = 0
    ) -> str:
    return compile(regex).sub(repl, string, count)
