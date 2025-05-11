from typing import Iterable
import re


def unions(table: Iterable[str]) -> str:
    return '|'.join(
        re.escape(k) for k in sorted(table, key=lambda x: -len(x))
    )


class Position():
    def __init__(self, column: int, line: int) -> None:
        self.column: int = column
        self.line: int = line
    
    def __str__(self) -> str:
        return f"<line: {self.line}; column: {self.column}>"

