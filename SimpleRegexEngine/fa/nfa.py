from typing import Iterator, Union
from .utils import ANY, fa_condition


class Node():
    def __init__(self):
        self.next: dict[fa_condition, list[Node]] = {}
        self.subset: set["Node"] = None
    
    def __setitem__(self, condition: fa_condition, node: "Node") -> None:
        if not isinstance(condition, fa_condition):
            raise TypeError("only allow string or [ANY]")
        if len(condition) > 1:
            raise ValueError("condition too long")
        if condition in self.next:
            self.next[condition].append(node)
        else:
            self.next[condition] = [node]

    def __getitem__(self, condition: str) -> Union[list["Node"], None]:
        return self.next.get(condition) or self.next.get(ANY)
    
    def __iter__(self) -> Iterator[fa_condition]:
        return iter(self.next)
    
    def get_subset(self) -> set["Node"]:
        if self.subset:
            return self.subset
        subset = {self}
        if '' in self.next:
            for node in self.next['']:
                subset = subset.union(node.get_subset())
        self.subset = subset
        return subset


class NFA():
    "non-deterministic finite automat"
    def __init__(self, head: Node, tail: Node):
        self.head: Node = head
        self.tail: Node = tail
    
    def __repr__(self) -> str:
        ft = nfa2fivetuple(self)
        return "\n".join(f"{i}: {ft[i]}" for i in ft)
    
    @classmethod
    def singlechar(cls, char: str) -> "NFA":
        """create a NFA like `s0 -char-> s1`"""
        s0 = Node()
        s1 = Node()
        s0[char] = s1
        return NFA(head=s0, tail=s1)
    
    @classmethod
    def epsilon(cls) -> "NFA":
        """create a NFA like `s0 -ε-> s1`"""
        s0 = Node()
        s1 = Node()
        s0[''] = s1
        return NFA(head=s0, tail=s1)
    
    @classmethod
    def anychar(cls) -> "NFA":
        """create a NFA like `s0 -<any>-> s1`"""
        s0 = Node()
        s1 = Node()
        s0[ANY] = s1
        return NFA(head=s0, tail=s1)

    @classmethod
    def concats(cls, *items: Union[str, "NFA"]) -> "NFA":
        nfa = cls.epsilon()
        for i in range(len(items)):
            match items[i]:
                case str():
                    nfa = nfa.concat(cls.singlechar(items[i]))
                case NFA():
                    nfa = nfa.concat(items[i])
                case _:
                    raise TypeError(f"unsupport Type: {type(items[i])}")
        return nfa

    @classmethod
    def unions(cls, *items: Union[str, "NFA"]) -> "NFA":
        nfa = cls.epsilon()
        for i in range(len(items)):
            match items[i]:
                case str():
                    nfa = nfa.union(cls.singlechar(items[i]))
                case NFA():
                    nfa = nfa.union(items[i])
                case _:
                    raise TypeError(f"unsupport Type: {type(items[i])}")
        return nfa

    def concat(self, nfa: "NFA") -> "NFA":
        """concat self to the specified NFA, and return result"""
        s0 = self.head
        s1 = self.tail
        s2 = nfa.head
        s3 = nfa.tail

        s1[''] = s2

        return NFA(head=s0, tail=s3)
    
    def union(self, nfa: "NFA") -> "NFA":
        """union self to the specified NFA, and return result"""
        s0 = self.head
        s0_ = nfa.head
        s1 = self.tail
        s2 = nfa.tail
        s3 = Node()

        for condition in s0_:
            for n in s0_[condition]:
                s0[condition] = n
        s1[''] = s3
        s2[''] = s3
        
        return NFA(head=s0, tail=s3)

    def closure(self) -> "NFA":
        """return self's closure"""
        s0 = self.head
        s1 = self.tail
        s2 = Node()

        s0[''] = s2
        s1[''] = s0

        return NFA(head=s0, tail=s2)


def nfa2fivetuple(nfa: NFA) -> dict:
    total: dict[Node, int] = {nfa.head: 0, nfa.tail: 1}
    transition_map: dict[int, dict[str, list]] = {}
    conds: set[str] = set()

    queue: list[Node] = [nfa.head]
    while len(queue):
        node = queue.pop()
        transition_map[total[node]] = {}
        for cond in node:
            c = str(cond)
            conds.add(c)
            transition_map[total[node]][c] = []
            for next_node in node[cond]:
                transition_map[total[node]][c].append(next_node)
                if next_node in total:
                    continue
                total[next_node] = len(total)
                queue.append(next_node)

    for node in transition_map:
        for cond in transition_map[node]:
            nexts = []
            for nfa_node in transition_map[node][cond]:
                nexts.append(total[nfa_node])
            transition_map[node][cond] = nexts

    return {
        "S": set(total.values()),
        "∑": conds,
        "s0": 0,
        "F": {1,},
        "M": transition_map
    }
