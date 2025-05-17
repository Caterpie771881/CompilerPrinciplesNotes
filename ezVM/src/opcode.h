#ifndef OPCODE_H
#define OPCODE_H

#include <cstdint>
#include <string>
#include <vector>
#include <tuple>

typedef uint8_t Opcode;
typedef std::vector<uint8_t> Instructions;

struct Definition
{
    std::string Name;
    std::vector<int> OperandWidths;
    Definition(std::string, std::vector<int>);
};

const Opcode OpConstant = 0;

Definition Lookup(Opcode op);

std::vector<uint8_t> Make(Opcode op, const std::vector<int> &operands);

std::tuple<std::vector<int>, int> ReadOperands(const Definition &, const Instructions &);

#endif