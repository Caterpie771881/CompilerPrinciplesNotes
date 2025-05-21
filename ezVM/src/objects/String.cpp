#include <iostream>
#include "object.h"

using namespace obj;

String::String()
    : value("") {}

String::String(std::string value)
    : value(value) {}

ObjectType String::Type() const
{
    return STRING_OBJ;
}

std::string String::Inspect() const
{
    return "'" + value + "'";
}

String *String::Add(Object *o)
{
    if (o->Type() == STRING_OBJ)
    {
        auto result = this->value + dynamic_cast<String *>(o)->value;
        return new String(result);
    }
    else if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value + dynamic_cast<Integer *>(o)->Inspect();
        return new String(result);
    }
    std::cerr << "'Interger' type can not add with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}
