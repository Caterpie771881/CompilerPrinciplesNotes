import re
from enum import StrEnum
from enum import auto
import warnings
from .syntax import STATEMENT, LABLE_ONLY
from .syntax import Statement
from .syntax import Token
from .syntax import Lable, Opcode, Operand
from .syntax import OpcodeDef
import math


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
            for i in re.split(r"\s+", stmt.group(4)):
                operand = Token.makeOperand(i)
                if operand:
                    operands.append(operand)
        
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
            print(code)
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
                code += self.get_operand_value(constID).to_bytes(2)
            # pseudoinstruction
            case Opcode.INT:
                value = operands[0]
                v = self.get_operand_value(value)
                length = math.ceil(v.bit_length() / 8)
                code += length.to_bytes(1)
                code += v.to_bytes(length)
            case Opcode.STRING:
                value = operands[0]
                v = self.get_operand_value(value)
                length = math.ceil(v.bit_length() / 8)
                code += length.to_bytes(2)
                code += v.to_bytes(length)
        return code

    def get_operand_value(self, operand: Token) -> int:
        literal = operand.literal
        match operand.type:
            case Operand.INT:
                return int(literal)
            case Operand.HEX:
                return int(literal, 16)
            case Operand.STRING:
                return int(literal[1:-1].encode('utf-8').hex(), 16)
            case Operand.LABLE:
                lable_line = self.symbols.get(literal)
                if not lable_line:
                    raise SyntaxError(f"no such lable: {literal}")
                return lable_line

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
