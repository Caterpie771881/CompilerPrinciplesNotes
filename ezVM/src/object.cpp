#include "object.h"

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
