#ifndef EZVM_H
#define EZVM_H

#include "opcode.h"
#include "object.h"
#include <vector>

struct Bytecode
{
    code::Instructions Instructions;
    std::vector<obj::Object *> Constants;
};

const int StackSize = 2048;

class VM
{
public:
    VM(const Bytecode &);
    obj::Object *StackTop();
    void Run();
    void Push(obj::Object *);
    obj::Object *Pop();

private:
    std::vector<obj::Object *> constants;
    code::Instructions instructions;
    std::vector<obj::Object *> stack;
    size_t sp;
};

#endif