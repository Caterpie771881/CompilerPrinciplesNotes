import re
from enum import StrEnum, auto


class AsmRule():
    def __init__(self, rules: dict[str, str]):
        self.rules: dict[str, str] = rules
        self._regex: str = ''

    @property
    def regex(self) -> str:
        if not self._regex:
            sorted_rule = sorted(self.rules.values(), key=lambda x: -len(x))
            self._regex = f"({'|'.join(i for i in sorted_rule)})"
        return self._regex


class OpcodeDef():
    _definitions: dict[str, "OpcodeDef"] = {}

    def __init__(
            self,
            name: str,
            pattern: str,
            code: bytes,
            operand_widths: list[int | str]
        ) -> None:
        self.name: str = name
        self.pattern: str = pattern
        self.code: bytes = code
        self.operand_num: list[int | str] = operand_widths
        self._definitions[name] = self
    
    @classmethod
    def export_rule(cls) -> AsmRule:
        rules: dict[str, str] = {}
        for _def in cls._definitions.values():
            rules[_def.name] = _def.pattern
        return AsmRule(rules)

    @classmethod
    def get(cls, name: str):
        return cls._definitions.get(name)


class Lable(StrEnum):
    CONST       = auto()
    INSTRUCTION = auto()
    LABLE       = auto()


class Opcode(StrEnum):
    CONST   = auto()
    ADD     = auto()
    POP     = auto()
    EXIT    = auto()
    INT     = auto()


class Operand(StrEnum):
    INT     = auto()
    HEX     = auto()
    STRING  = auto()
    LABLE   = auto()


LableRule: AsmRule = AsmRule({
    Lable.CONST         : r"\.cnst:",
    Lable.INSTRUCTION   : r"\.inst:",
    Lable.LABLE         : r"[._a-zA-Z0-9]*:",
})

OpcodeDef(Opcode.CONST, r"const",   b'\x01', 1)
OpcodeDef(Opcode.ADD,   r"add",     b'\x02', 0)
OpcodeDef(Opcode.POP,   r"pop",     b'\x03', 0)
OpcodeDef(Opcode.EXIT,  r"exit",    b'\xff', 0)
OpcodeDef(Opcode.INT,   r"\.int",   b'\x01', 1)
OpcodeRule: AsmRule = OpcodeDef.export_rule()

OperandRule: AsmRule = AsmRule({
    Operand.INT     : r"\d+",
    Operand.HEX     : r"0x[\da-fA-F]+",
    Operand.STRING  : r"'.*?'|\".*?\"",
    Operand.LABLE   : r"[._a-zA-Z0-9]*",
})

STATEMENT = re.compile(
    fr"({LableRule.regex}\s*)?{OpcodeRule.regex}((\s+{OperandRule.regex})*)")
LABLE_ONLY = re.compile(LableRule.regex)


class Token():
    def __init__(self, type_: str, literal: str):
        self.type: str = type_
        self.literal: str = literal

    @staticmethod
    def _makeToken(string: str | None, rule: AsmRule) -> "Token":
        if not string:
            return None
        for type_, pattern in rule.rules.items():
            m = re.match(pattern, string)
            if m and m.end() == len(string):
                return Token(type_, string)
        return None
    
    @classmethod
    def makeLable(cls, string: str) -> "Token":
        return cls._makeToken(string, LableRule)

    @classmethod
    def makeOpcode(cls, string: str) -> "Token":
        return cls._makeToken(string, OpcodeRule)
    
    @classmethod
    def makeOperand(cls, string: str) -> "Token":
        return cls._makeToken(string, OperandRule)


class Statement():
    def __init__(
            self,
            line: int,
            lable: Token | None,
            opcode: Token | None,
            operands: list[Token]
        ) -> None:
        self.line: int = line
        self.lable: Token = lable
        self.opcode: Token = opcode
        self.operands: list[Token] = operands

