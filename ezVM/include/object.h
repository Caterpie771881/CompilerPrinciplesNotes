#ifndef OBJECT_H
#define OBJECT_H

#include <string>
#include <cstdint>
#include <vector>
#include <tuple>

namespace obj
{
    typedef std::string ObjectType;
    typedef std::vector<uint8_t> ConstsPool;

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
        virtual Object *Add(Object *);
        virtual Object *Sub(Object *);
        virtual Object *Mul(Object *);
        virtual Object *Div(Object *);
        // virtual Bool *Eq(Object *);
        // virtual Bool *Gt(Object *);
    private:
        virtual void UnsupportOperateError(const std::string &);
    };

    class Integer : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        long long value;
        Integer(long long);
        Integer *Add(Object *) override;
        Integer *Sub(Object *) override;
        Integer *Mul(Object *) override;
        Integer *Div(Object *) override;
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
    const None _None = None();

    class String : public Object
    {
    public:
        ObjectType Type() const override;
        std::string Inspect() const override;
        String();
        String(std::string);
        std::string value;
        String *Add(Object *) override;
    };

    ObjectTypeEnum LookupConst(uint8_t);

    std::tuple<Object *, int> ReadConst(ConstsPool, size_t);
} // namespace obj

#endif