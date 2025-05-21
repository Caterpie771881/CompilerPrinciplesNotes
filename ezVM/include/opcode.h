#ifndef OPCODE_H
#define OPCODE_H

#include <cstdint>
#include <string>
#include <vector>
#include <tuple>

namespace code
{
    typedef uint8_t Opcode;
    typedef std::vector<uint8_t> Instructions;

    struct Definition
    {
        std::string Name;
        std::vector<int> OperandWidths;
        Definition(std::string, std::vector<int>);
    };

    const Opcode OpNop = 0x00;
    const Opcode OpConstant = 0x01;
    const Opcode OpAdd = 0x02;
    const Opcode OpPop = 0x03;
    const Opcode OpSub = 0x04;
    const Opcode OpMul = 0x05;
    const Opcode OpDiv = 0x06;
    const Opcode OpTrue = 0x07;
    const Opcode OpFalse = 0x08;
    const Opcode OpEq = 0x09;
    const Opcode OpNe = 0x0a;
    const Opcode OpGt = 0x0b;
    const Opcode OpMinus = 0x0c;
    const Opcode OpBang = 0x0d;
    const Opcode OpJump = 0x0e;
    const Opcode OpJnt = 0x0f;
    const Opcode OpNone = 0x10;
    const Opcode OpGetGlobal = 0x11;
    const Opcode OpSetGlobal = 0x12;
    const Opcode OpArray = 0x13;
    const Opcode OpHash = 0x14;
    const Opcode OpIndex = 0x15;
    const Opcode OpCall = 0x16;
    const Opcode OpReturn = 0x17;
    const Opcode OpReturnValue = 0x18;
    const Opcode OpGetLocal = 0x19;
    const Opcode OpSetLocal = 0x1a;
    const Opcode OpBuiltin = 0x1b;
    const Opcode OpEnd = 0xff;

    Definition Lookup(Opcode op);

    std::vector<uint8_t> Make(Opcode op, const std::vector<int> &operands);

    std::tuple<std::vector<int>, int> ReadOperands(const Definition &, const Instructions &, size_t);
} // namespace code

#endif