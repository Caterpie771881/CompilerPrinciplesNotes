#include <iostream>
#include "ezVM.h"
#include "utils.h"

VM::VM(const Bytecode &bytecode)
    : instructions(bytecode.Instructions),
      constants(bytecode.Constants),
      stack(std::vector<obj::Object *>(StackSize, nullptr)),
      sp(0)
{
}

obj::Object *VM::StackTop()
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
        code::Opcode op = instructions[ip];
        switch (op)
        {
        case code::OpConstant:
        {
            std::cout << "doing constant" << std::endl;
            uint16_t constIndex = ReadUint16(instructions, ip + 1);
            ip += 2;
            this->Push(constants.at(constIndex));
            break;
        }
        case code::OpAdd:
        {
            std::cout << "doing add" << std::endl;
            auto right = this->Pop();
            auto left = this->Pop();
            auto result = right->_add_(left);
            if (result)
                this->Push(result);
            else
                return;
            break;
        }
        case code::OpEnd:
            return;
        }
    }
}

void VM::Push(obj::Object *o)
{
    if (sp >= StackSize)
    {
        throw "stack overflow";
    }
    stack[sp] = o;
    sp++;
}

obj::Object *VM::Pop()
{
    obj::Object *o = stack[sp - 1];
    std::cout << "sp: " << std::to_string(sp)
              << "; will pop: " << o->Inspect() << std::endl;
    sp--;
    return o;
}
