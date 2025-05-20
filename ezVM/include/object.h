#ifndef OBJECT_H
#define OBJECT_H

#include <string>
#include <cstdint>
#include <vector>
#include <tuple>

namespace obj
{
    typedef std::string ObjectType;
    typedef std::vector<uint8_t> ObjectPool;

    enum ObjectTypeEnum
    {
        Enum_NOTHING,
        Enum_INTEGER_OBJ,
        Enum_BOOL_OBJ,
        Enum_NONE_OBJ,
        Enum_STRING_OBJ,
        Enum_CUSTOM_OBJ,
    };

    const ObjectType INTEGER_OBJ = "INTERGER";
    const ObjectType BOOL_OBJ = "BOOL";
    const ObjectType NONE_OBJ = "NONE";
    const ObjectType STRING_OBJ = "STRING";
    const ObjectType CUSTOM_OBJ = "CUSTOM";

    class Object
    {
    public:
        virtual ObjectType Type() const = 0;
        virtual std::string Inspect() const = 0;
        virtual ~Object() = default;
        virtual Object *_add_(Object *);
        // virtual Object *_eq_(Object *);
        // virtual Object *_gt_(Object *);
    };

    class Integer : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        long long value;
        Integer(long long);
        Integer *_add_(Object *) override;
    };

    class Bool : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        bool value;
        Bool(bool);
    };
    const Bool True = Bool(true);
    const Bool False = Bool(false);

    class None : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        None();
    };
    const None none = None();

    class String : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        String();
        String(std::string);
        std::string value;
        String *_add_(Object *) override;
    };

    std::tuple<Object *, int> ReadObject(uint8_t, ObjectPool);
} // namespace obj

#endif