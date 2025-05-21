#include "object.h"

using namespace obj;

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
