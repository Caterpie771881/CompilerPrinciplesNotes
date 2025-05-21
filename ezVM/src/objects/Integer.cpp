#include <iostream>
#include "object.h"

using namespace obj;

Integer::Integer(long long value)
    : value(value) {}

ObjectType Integer::Type() const
{
    return INTEGER_OBJ;
}

std::string Integer::Inspect() const
{
    return std::to_string(this->value);
}

Integer *Integer::Add(Object *o)
{
    if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value + dynamic_cast<Integer *>(o)->value;
        return new Integer(result);
    }
    std::cerr << "'Interger' type can not add with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}

Integer *Integer::Sub(Object *o)
{
    if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value - dynamic_cast<Integer *>(o)->value;
        return new Integer(result);
    }
    std::cerr << "'Interger' type can not sub with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}

Integer *Integer::Mul(Object *o)
{
    if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value * dynamic_cast<Integer *>(o)->value;
        return new Integer(result);
    }
    std::cerr << "'Interger' type can not mul with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}

Integer *Integer::Div(Object *o)
{
    if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value / dynamic_cast<Integer *>(o)->value;
        return new Integer(result);
    }
    std::cerr << "'Interger' type can not div with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}
