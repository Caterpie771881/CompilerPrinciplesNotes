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
        return f"S: {ft['S']}\n∑: {ft['∑']}\ns0: {ft['s0']}\nF: {ft['F']}\nM: {ft['M']}"
    
    def match(self, string: str) -> bool:
        node = self.head
        for char in string:
            node = node[char]
            if not node:
                return False
        return node.end

    # TODO
    def find(self, string: str) -> Union[str, None]:
        raise Exception("todo")
    
    # TODO
    def findall(self, string: str) -> list[str]:
        raise Exception("todo")
    
    # TODO
    def split(self, string: str) -> list[str]:
        raise Exception("todo")
    
    # TODO
    def sub(self, string: str, repl: str) -> str:
        raise Exception("todo")


def dfa2fivetuple(dfa: DFA) -> str:
    total: dict[Node, int] = {dfa.head: 0}
    transition_map: dict[int, dict[str, Union[Node, int]]] = {}
    conds: set[str] = set()

    queue: list[Node] = [dfa.head]
    while len(queue):
        node = queue.pop()
        transition_map[total[node]] = {}
        for cond in node:
            c = '<any>' if cond is ANY else cond
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
