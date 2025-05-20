#include "object.h"
#include <iostream>
#include <map>

using namespace obj;

std::map<uint8_t, ObjectTypeEnum> definitions = {
    {0x00, Enum_NOTHING},
    {0x01, Enum_INTEGER_OBJ},
    {0x02, Enum_STRING_OBJ},
    {0xff, Enum_CUSTOM_OBJ},
};

Object *Object::_add_(Object *o)
{
    std::cerr << "type '" << this->Type() << "' unsupport add operate" << std::endl;
    return nullptr;
}

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

Integer *Integer::_add_(Object *o)
{
    if (o->Type() == INTEGER_OBJ)
    {
        auto result = this->value + dynamic_cast<Integer *>(o)->value;
        return new Integer(result);
    }
    std::cerr << "'Interger' type can not add with: '" << o->Type() << "'" << std::endl;
    return nullptr;
}

Bool::Bool(bool value)
    : value(value) {}

ObjectType Bool::Type() const
{
    return BOOL_OBJ;
}

std::string Bool::Inspect() const
{
    if (this->value == true)
    {
        return "True";
    }
    else
    {
        return "False";
    }
}

None::None() {}

ObjectType None::Type() const
{
    return NONE_OBJ;
}

std::string None::Inspect() const
{
    return "None";
}

std::tuple<Object *, int> ReadObject(uint8_t code, ObjectPool pool)
{
    int offset = 0;
    ObjectTypeEnum type;
    try
    {
        type = definitions.at(code);
    }
    catch (const std::exception &e)
    {
        std::cerr << "unknown object type" << std::endl;
        return {nullptr, 0};
    }

    switch (type)
    {
    case Enum_INTEGER_OBJ:

        break;
    case Enum_STRING_OBJ:
        break;
    case Enum_CUSTOM_OBJ:
        break;
    case Enum_NOTHING:
        return {nullptr, 1};
        break;
    }

    return {(Object *)&none, offset};
}
