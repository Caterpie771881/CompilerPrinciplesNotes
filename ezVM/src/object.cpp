#include <iostream>
#include <map>
#include <cstring>
#include "utils.h"
#include "object.h"

using namespace obj;

std::map<uint8_t, ObjectTypeEnum> constdef = {
    {0x00, Enum_NOTHING},
    {0x01, Enum_INTEGER_OBJ},
    {0x02, Enum_STRING_OBJ},
    {0xff, Enum_CUSTOM_OBJ},
};

ObjectTypeEnum obj::LookupConst(uint8_t code)
{
    try
    {
        return constdef.at(code);
    }
    catch (const std::exception &e)
    {
        std::string err = "unknown const type";
        std::cerr << err << std::endl;
        throw err;
    }
}

void Object::UnsupportOperateError(const std::string &optype)
{
    std::cerr << "type '"
              << Type()
              << "' unsupport"
              << optype
              << "operate"
              << std::endl;
}

Object *Object::Add(Object *o)
{
    UnsupportOperateError("addition");
    return nullptr;
}

Object *Object::Sub(Object *o)
{
    UnsupportOperateError("subtraction");
    return nullptr;
}

Object *Object::Mul(Object *o)
{
    UnsupportOperateError("multiplication");
    return nullptr;
}

Object *Object::Div(Object *o)
{
    UnsupportOperateError("division");
    return nullptr;
}

std::tuple<Object *, int> obj::ReadConst(ConstsPool pool, size_t index = 0)
{
    int offset = 0;

    switch (LookupConst(pool[index]))
    {
    case Enum_INTEGER_OBJ:
    {
        uint8_t length;
        long long value;
        uint8_t buffer[8] = {0};

        length = pool[index + 1];
        offset += 1 + length;
        if (index + offset > pool.size())
        {
            std::cerr << "const pool overflow! file is corrupt" << std::endl;
            return {nullptr, 1};
        }
        std::memcpy(buffer, &pool[index + 2], length);
        std::memcpy(&value, buffer, sizeof(long long));

        return {new Integer(value), offset};
        break;
    }
    case Enum_STRING_OBJ:
    {
        uint16_t length;
        std::string value("");

        length = ReadUint16(pool, index + 1);
        offset += 2 + length;
        if (index + offset > pool.size())
        {
            std::cerr << "const pool overflow! file is corrupt" << std::endl;
            return {nullptr, 1};
        }
        value.assign(reinterpret_cast<char *>(&pool[index + 3]), length);

        return {new String(value), offset};
        break;
    }
    case Enum_CUSTOM_OBJ:
    {
        break;
    }
    case Enum_NOTHING:
    {
        return {nullptr, 1};
        break;
    }
    }

    return {(Object *)&_None, 1};
}
