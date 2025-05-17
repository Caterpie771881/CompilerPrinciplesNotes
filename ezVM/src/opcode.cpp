#include "opcode.h"
#include <map>
#include <sstream>
#include "utils.h"


Definition::Definition(std::string name, std::vector<int> opWidths) 
    : Name(name), OperandWidths(opWidths) {}


std::map<Opcode, Definition> definitions = {
    {OpConstant, Definition("OpConstant", std::vector<int>{2})},
};


Definition Lookup(Opcode op) {
    try {
        return definitions.at(op);
    }
    catch(const std::exception& e) {
        std::stringstream err;
        err << "opcode " << op << " undefined";
        throw err.str();
    }
}


Instructions Make(Opcode op, std::vector<int> operands) {
    Definition def = Lookup(op);
    int instructionLen = 1;

    for (int w: def.OperandWidths) {
        instructionLen += w;
    }

    Instructions instruction(instructionLen, 0U);
    instruction[0] = op;

    int offset = 1;
    for (int i = 0; i < operands.size(); i++) {
        int width = def.OperandWidths[i];
        int operand = operands[i];
        switch (width) {
        case 2:
            PutUint16(instruction, offset, (uint16_t)operand);
            break;
        }
        offset += width;
    }
    return instruction;
}
