#ifndef OBJECT_H
#define OBJECT_H

#include <string>

typedef std::string ObjectType;

const ObjectType INTEGER_OBJ = "INTERGER";
const ObjectType BOOL_OBJ = "BOOL";
const ObjectType NONE_OBJ = "NONE";

class Object
{
public:
    virtual ObjectType Type() const = 0;
    virtual std::string Inspect() const = 0;
    virtual ~Object() = default;
};

class Integer : public Object
{
public:
    ObjectType Type() const override;
    std::string Inspect() const override;
    long long value;
    Integer(long long);
};

class Bool : public Object
{
public:
    ObjectType Type() const override;
    std::string Inspect() const override;
    bool value;
    Bool(bool);
};

class None : public Object
{
public:
    ObjectType Type() const override;
    std::string Inspect() const override;
    None();
};

#endif