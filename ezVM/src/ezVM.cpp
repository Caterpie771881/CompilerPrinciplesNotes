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
        case code::OpNop:
            break;
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
            auto result = left->Add(right);
            // delete left; delete right;
            if (result)
                this->Push(result);
            else
                return;
            break;
        }
        case code::OpPop:
        {
            this->Pop();
            // delete this->Pop();
            break;
        }
        case code::OpEnd:
            return;
        default:
            std::cerr << "unknown opcode: " << std::to_string(op) << std::endl;
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
    obj::Object *o = this->StackTop();
    std::string inspect = "[NOTHING '']";
    if (o)
        inspect = "[" + o->Type() + " " + o->Inspect() + "]";
    std::cout << "sp: " << std::to_string(sp)
              << "; will pop: " << inspect << std::endl;
    sp--;
    return o;
}
