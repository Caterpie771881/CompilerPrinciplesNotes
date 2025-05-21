#include "opcode.h"
#include <map>
#include <sstream>
#include "utils.h"
#include <iostream>

using namespace code;

Definition::Definition(std::string name, std::vector<int> opWidths)
    : Name(name), OperandWidths(opWidths) {}

std::map<Opcode, Definition> constdef = {
    {OpConstant, Definition("OpConstant", {2})},
    {OpAdd, Definition("OpAdd", {})},
};

Definition code::Lookup(Opcode op)
{
    try
    {
        return constdef.at(op);
    }
    catch (const std::exception &e)
    {
        std::stringstream err;
        err << "opcode '" << std::to_string(op) << "' undefined";
        std::cerr << err.str() << std::endl;
        throw err.str();
    }
}

std::vector<uint8_t> code::Make(Opcode op, const std::vector<int> &operands)
{
    Definition def = Lookup(op);
    int instructionLen = 1;
    for (int w : def.OperandWidths)
    {
        instructionLen += w;
    }

    std::vector<uint8_t> instruction(instructionLen, 0);
    instruction[0] = op;

    size_t offset = 1;
    for (size_t i = 0; i < operands.size(); i++)
    {
        int width = def.OperandWidths[i];
        int operand = operands[i];
        switch (width)
        {
        case 2:
            PutUint16(instruction, offset, (uint16_t)operand);
            break;
        }
        offset += width;
    }
    return instruction;
}

std::tuple<std::vector<int>, int> code::ReadOperands(const Definition &def, const Instructions &ins, size_t index = 0)
{
    std::vector<int> operands(def.OperandWidths.size(), 0);
    int offset = 0;

    for (size_t i = 0; i < def.OperandWidths.size(); i++)
    {
        int width = def.OperandWidths[i];
        switch (width)
        {
        case 2:
            operands[i] = (int)ReadUint16(ins, offset + index);
            break;
        }
        offset += width;
    }
    return {operands, offset};
};
