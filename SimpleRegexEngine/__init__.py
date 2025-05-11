from .compiler import *
from typing import Union


def match(regex: str, string: str) -> bool:
    return compile(regex).match(string)


def find(regex: str, string: str) -> Union[str, None]:
    return compile(regex).find(string)


def findall(regex: str, string: str) -> list[str]:
    return compile(regex).findall(string)
    

def split(regex: str, string: str) -> list[str]:
    return compile(regex).split(string)


def sub(regex: str, string: str, repl: str) -> str:
    return compile(regex).sub(string, repl)
