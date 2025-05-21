#include "object.h"

using namespace obj;

None::None() {}

ObjectType None::Type() const
{
    return NONE_OBJ;
}

std::string None::Inspect() const
{
    return "None";
}
