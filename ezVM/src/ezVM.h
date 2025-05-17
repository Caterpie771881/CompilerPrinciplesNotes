#ifndef EZVM_H
#define EZVM_H

#include "opcode.h"
#include "object.h"
#include <vector>

struct Bytecode
{
    Instructions Instructions;
    std::vector<Object *> Constants;
};

const int StackSize = 2048;

class VM
{
public:
    VM(Bytecode &);
    Object *StackTop();
    void Run();
    void Push(Object &);

private:
    std::vector<Object *> constants;
    Instructions instructions;
    std::vector<Object *> stack;
    size_t sp;
};

#endif