#include <iostream>
#include "ezVM.h"
#include "utils.h"

VM::VM(Bytecode &bytecode)
    : instructions(bytecode.Instructions),
      constants(bytecode.Constants),
      stack(std::vector<Object *>(StackSize, nullptr)),
      sp(0)
{
}

Object *VM::StackTop()
{
    if (sp == 0)
    {
        return nullptr;
    }
    return stack[sp - 1];
}

void VM::Run()
{
    for (size_t ip = 0; ip < instructions.size(); ip++)
    {
        Opcode op = instructions[ip];
        switch (op)
        {
        case OpConstant:
            uint16_t constIndex = ReadUint16(instructions, ip + 1);
            ip += 2;
            this->Push(*constants[constIndex]);
            break;
        }
    }
}

void VM::Push(Object &o)
{
    if (sp >= StackSize)
    {
        throw "stack overflow";
    }
    stack[sp] = &o;
    sp++;
}