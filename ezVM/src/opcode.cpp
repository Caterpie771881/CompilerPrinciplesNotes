#include "opcode.h"
#include <map>
#include <sstream>
#include "utils.h"

Definition::Definition(std::string name, std::vector<int> opWidths)
    : Name(name), OperandWidths(opWidths) {}

std::map<Opcode, Definition> definitions = {
    {OpConstant, Definition("OpConstant", std::vector<int>{2})},
};

Definition Lookup(Opcode op)
{
    try
    {
        return definitions.at(op);
    }
    catch (const std::exception &e)
    {
        std::stringstream err;
        err << "opcode " << op << " undefined";
        throw err.str();
    }
}

std::vector<uint8_t> Make(Opcode op, const std::vector<int> &operands)
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

std::tuple<std::vector<int>, int> ReadOperands(const Definition &def, const Instructions &ins)
{
    std::vector<int> operands(def.OperandWidths.size(), 0);
    int offset = 0;

    for (size_t i = 0; i < def.OperandWidths.size(); i++)
    {
        int width = def.OperandWidths[i];
        switch (width)
        {
        case 2:
            operands[i] = (int)ReadUint16(ins, i);
            break;
        }
        offset += width;
    }
    return {operands, offset};
};
