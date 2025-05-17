#ifndef OPCODE_H
#define OPCODE_H

#include <cstdint>
#include <string>
#include <vector>

typedef uint8_t Opcode;
typedef std::vector<uint8_t> Instructions;

struct Definition {
    std::string         Name;
    std::vector<int>    OperandWidths;
    Definition(std::string, std::vector<int>);
};

const Opcode OpConstant = 0;

Definition Lookup(Opcode op);

std::vector<uint8_t> Make(Opcode op, std::vector<int> operands);

#endif