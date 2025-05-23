import re
from enum import StrEnum
from enum import auto
import warnings
from .syntax import STATEMENT
from .syntax import LABLE_ONLY
from .syntax import Statement
from .syntax import Token
from .syntax import Lable
from .syntax import Opcode
from .syntax import Operand
from .syntax import OpcodeDef


class Section(StrEnum):
    CONST = auto()
    INSTRUCTION = auto()


class Assambler():
    MAGIC = b"\x65\x7a\x76\x6d"
    EOF = b"\x00\x65\x6f\x66"

    def __init__(self, codes: list[str]) -> None:
        self.codes: list[str] = codes
        self.stmts: list[Statement] = []
        self.constpool: bytes = b''
        self.instructions: bytes = b''
        self.cur_section: Section = Section.CONST
        self.symbols: dict[str, int] = {}
    
    def prepare_stmts(self) -> None:
        for i in range(len(self.codes)):
            lable, opcode, operands = self.parse_line(self.codes[i])
            if not lable and not opcode:
                continue
            self.stmts.append(Statement(i, lable, opcode, operands))
    
    def build_symbols(self) -> None:
        for stmt in self.stmts:
            label = stmt.lable
            if not label:
                continue
            self.symbols[label] = stmt.line
    
    def parse_line(self, line: str) -> tuple[Token, Token, list[Token]]:
        lable: Token = None
        opcode: Token = None
        operands: list[Token] = []

        line = line.strip('\n\r\t ')
        if not line:
            return None, None, []
        
        stmt = STATEMENT.match(line)
        lable_only = LABLE_ONLY.match(line)

        if stmt and stmt.end() > len(line)-1:
            lable = Token.makeLable(stmt.group(2))
            opcode = Token.makeOpcode(stmt.group(3))
            for i in re.split(r"\s+", stmt.group(4))[1:]:
                operands.append(Token.makeOperand(i))
        
        elif lable_only and lable_only.end() > len(line)-1:
            lable = Token.makeLable(lable_only.group())
        
        else:
            warnings.warn(f"\n{line}\nis illegal, will skip it", SyntaxWarning)
        
        return lable, opcode, operands

    def parse_stmt(self, stmt: Statement) -> None:
        lable = stmt.lable
        opcode = stmt.opcode
        operands = stmt.operands
        if lable:
            self.parse_lable(lable)
        if opcode:
            code = self.parse_opcode(opcode, operands)
            match self.cur_section:
                case Section.CONST:
                    self.constpool += code
                case Section.INSTRUCTION:
                    self.instructions += code
    
    def parse_lable(self, lable: Token) -> None:
        match lable.type:
            case Lable.CONST:
                self.cur_section = Section.CONST
            case Lable.INSTRUCTION:
                self.cur_section = Section.INSTRUCTION
    
    def parse_opcode(self, opcode: Token, operands: list[Token]) -> bytes:
        code = b''
        opdef = OpcodeDef.get(opcode.type)
        if not opdef or len(operands) != opdef.operand_num:
            return b''
        code += opdef.code
        if not opdef.operand_num:
            return code
        match opdef.name:
            case Opcode.CONST:
                constID = operands[0]
                match constID.type:
                    case Operand.INT:
                        code += int(constID.literal).to_bytes(2)
                    case Operand.HEX:
                        code += int(constID.literal[2:], 16).to_bytes(2)
                    case _:
                        ...
            # pseudoinstruction
            case Opcode.INT:
                value = operands[0]
                match value.type:
                    case Operand.INT:
                        v = int(value.literal)
                    case Operand.HEX:
                        v = int(value.literal, 16)
                    case _:
                        v = 0
                length = v.bit_count() // 4 + 1
                code += length.to_bytes(1)
                code += v.to_bytes(length)
        return code

    def get_fileheader(self) -> bytes:
        return (self.MAGIC
                + b'\x00\x01\x00\x00'
                + len(self.constpool).to_bytes(4)
                + len(self.instructions).to_bytes(4))
    
    def assamble(self) -> bytes:
        self.prepare_stmts()
        self.build_symbols()
        for stmt in self.stmts:
            self.parse_stmt(stmt)
        
        return (self.get_fileheader()
                + self.constpool
                + self.instructions
                + self.EOF)
