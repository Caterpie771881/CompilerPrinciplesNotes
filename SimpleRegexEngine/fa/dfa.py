from typing import Iterator, Union
from .utils import ANY, fa_condition


class Node():
    def __init__(self, end: bool = False):
        self.next: dict[fa_condition, Node] = {}
        self.end: bool = end
    
    def __setitem__(self, condition: fa_condition, node: "Node") -> None:
        if condition == '':
            raise KeyError("DFA unsupport epsilon condition")
        if not isinstance(condition, fa_condition):
            raise TypeError("only allow string")
        if len(condition) > 1:
            raise ValueError("condition too long")
        self.next[condition] = node
    
    def __getitem__(self, condition: str) -> Union["Node", None]:
        return self.next.get(condition) or self.next.get(ANY)
    
    def __iter__(self) -> Iterator[fa_condition]:
        return iter(self.next)


class DFA():
    "deterministic finite automat"
    def __init__(self, head: Node):
        self.head = head
    
    def __repr__(self) -> str:
        ft = dfa2fivetuple(self)
        return "\n".join(f"{i}: {ft[i]}" for i in ft)
    
    def match(self, string: str) -> str:
        node = self.head
        current = rem = ''
        for char in string:
            current += char
            node = node[char]
            if not node:
                return rem
            if node.end:
                rem = current
        return rem

    def find(self, string: str) -> Union[str, None]:
        for i in range(len(string)):
            m = self.match(string[i:])
            if m: return m
        return None
    
    def findall(self, string: str) -> list[str]:
        result = []
        i = 0
        while i < len(string):
            m = self.match(string[i:])
            if m:
                result.append(m)
                i += len(m)
            else:
                i += 1
        return result
    
    def split(self, string: str, maxsplit: int = 0) -> list[str]:
        if maxsplit < 0:
            return [string]
        result = []
        fp = bp = 0
        while bp < len(string):
            m = self.match(string[bp:])
            if m:
                result.append(string[fp: bp])
                bp += len(m)
                fp = bp
                if maxsplit and len(result) >= maxsplit:
                    break
            else:
                bp += 1
        result.append(string[fp:])
        return result
    
    def sub(self, repl: str, string: str, count: int = 0) -> str:
        if count < 0:
            return string
        result = ''
        fp = bp = c = 0
        while bp < len(string):
            m = self.match(string[bp:])
            if m:
                result += string[fp: bp] + repl
                bp += len(m)
                fp = bp
                c += 1
                if count and c >= count:
                    break
            else:
                bp += 1
        return result + string[fp:]


def dfa2fivetuple(dfa: DFA) -> dict:
    total: dict[Node, int] = {dfa.head: 0}
    transition_map: dict[int, dict[str, Union[Node, int]]] = {}
    conds: set[str] = set()

    queue: list[Node] = [dfa.head]
    while len(queue):
        node = queue.pop()
        transition_map[total[node]] = {}
        for cond in node:
            c = str(cond)
            conds.add(c)
            next_node = node[cond]
            transition_map[total[node]][c] = next_node
            if next_node in total:
                continue
            total[next_node] = len(total)
            queue.append(next_node)

    for node in transition_map:
        for cond in transition_map[node]:
            next_node: Node = transition_map[node][cond]
            transition_map[node][cond] = total[next_node]

    return {
        "S": set(total.values()),
        "∑": conds,
        "s0": 0,
        "F": set(total.get(n) for n in total if n.end),
        "M": transition_map
    }
