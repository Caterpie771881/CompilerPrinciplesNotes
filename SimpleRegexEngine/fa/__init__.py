from .nfa import NFA
from .dfa import DFA
from .utils import fa_condition


__all__ = ["NFA", "DFA", "subset_construction", "hopcroft"]


def subset_construction(nfa: NFA) -> DFA:
    from .nfa import Node as NFA_Node
    from .dfa import Node as DFA_Node

    class Task():
        def __init__(
                self,
                from_: DFA_Node = None,
                condition: str = '',
                to: NFA_Node = None
            ):
            self.from_ = from_
            self.condition = condition
            self.to = to
    
    def link(task: Task, to: DFA_Node) -> None:
        if task.from_:
            task.from_[task.condition] = to
    
    head: NFA_Node = None
    subsets: dict[frozenset[NFA_Node], DFA_Node] = {}
    queue: list[Task] = [Task(None, '', nfa.head)]

    while len(queue):
        task = queue.pop()
        subset = frozenset(task.to.get_subset())
        if subset in subsets:
            link(task, subsets[subset])
            continue
        dfa_node = DFA_Node(end=(nfa.tail in subset))
        subsets[subset] = dfa_node
        if not head: head = dfa_node
        link(task, dfa_node)
        for node in subset:
            for condition in node:
                if condition == '':
                    continue
                for next_node in node[condition]:
                    queue.append(Task(dfa_node, condition, next_node))

    return DFA(head)


def hopcroft(dfa: DFA) -> DFA:
    from .dfa import Node

    def split(s: set[Node], conds: set[fa_condition], total_sets: list[set[Node]]) -> list[set[Node]]:
        for c in conds:
            goto: dict[int, set[Node]] = {}
            for n in s:
                next_node = n[c]
                if next_node is None:
                    i = -1
                elif next_node in s:
                    i = -2
                else:
                    for i in range(len(total_sets)):
                        if next_node in total_sets[i]:
                            break
                if i not in goto:
                    goto[i] = set()
                goto[i].add(n)
            if len(goto) - 1:
                new_sets = list(goto.values())
                return new_sets
        return []
    
    def rebuild_dfa(total_sets: list[set[Node]]) -> DFA:
        head : Node            = None
        nodes: list[Node]      = []
        n2s  : dict[Node, int] = {}
        for i in range(len(total_sets)):
            s = total_sets[i]
            for n in s:
                n2s[n] = i
            new_node = Node(end=n.end)
            nodes.append(new_node)
            if not head and dfa.head in s:
                head = new_node
        for n in n2s:
            new_node = nodes[n2s[n]]
            for cond in n:
                old_next_node = n[cond]
                new_next_node = nodes[n2s[old_next_node]]
                new_node[cond] = new_next_node
        return DFA(head=head)

    total_states: set[Node]         = {dfa.head}
    end_set     : set[Node]         = set()
    notend_set  : set[Node]         = set()
    conds       : set[fa_condition] = set()
    total_sets  : list[set[Node]]   = [end_set, notend_set]
    
    queue: list[Node] = [dfa.head]
    while len(queue):
        node = queue.pop()
        if node.end:
            end_set.add(node)
        else:
            notend_set.add(node)
        for cond in node:
            conds.add(cond)
            next_node = node[cond]
            if next_node in total_states:
                continue
            total_states.add(next_node)
            queue.append(next_node)

    # try to split all sets util can not split any set
    tosplit: list[set[Node]] = [end_set, notend_set]
    while len(tosplit):
        s = tosplit.pop()
        new_sets = split(s, conds, total_sets)
        if new_sets:
            total_sets.remove(s)
            total_sets += new_sets
            tosplit += new_sets

    return rebuild_dfa(total_sets)
