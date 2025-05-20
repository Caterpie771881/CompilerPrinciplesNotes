# ezVM

ezVM 是 'easy virtual machine' 的缩写, 是一个用 C++17 实现的小型操作栈式虚拟机

携带了一个配套的汇编器 `assembler.py`

## 使用方法

编译虚拟机
```sh
mkdir build; cd build
cmake ..; make
```

编译一个简单的程序并执行
```
python3 assembler.py example/hello -o hello
./build/bin/ezVM hello
```

## 可执行文件格式定义

魔数0x657a766d\
虚拟机版本号(2bytes)\
常量池大小(4bytes)\
操作码大小(4bytes)\
常量池\
操作码\
结束符0x00656f66

## 指令支持

```
0x00                ;不执行任何操作
0x01 CONST n(2b)    ;从常量池中取出一个常量入栈, n为常量池元素编号
0x02 ADD            ;栈上加法
0x03 POP            ;弹出栈顶元素
0x04 SUB            ;栈上减法
0x05 MUL            ;栈上乘法
0x06 DIV            ;栈上除法
0x07 TRUE           ;将True常量入栈
0x08 FALSE          ;将False常量入栈
0x09 EQ             ;栈上相等运算
0x0A NEQ            ;栈上不等运算
0x0B GT             ;栈上大于运算
0x0C MINUS          ;栈上取负
0x0D BANG           ;栈上取非
0x0E JUMP n(2b)     ;无条件跳转
0x0F JNT  n(2b)     ;当栈顶不为真或空时跳转
0x10 NONE           ;将None常量入栈
0x11 GET n(2b)      ;从全局存储取出数据入栈
0x12 SET n(2b)      ;将栈顶元素绑定到全局存储
0x13 ARRAY n(2b)    ;弹出n个元素组成数组
0x14 HASH n(2b)     ;弹出栈内n*2个元素, 组成哈希表后入栈
0x15 INDEX          ;弹出两个元素, 第一个作为被索引对象, 第二个作为索引对象, 然后将索引结果压栈
0x16 CALL           ;弹出栈顶元素并作为函数执行
0x17 RETURN         ;函数返回
0x18 RETURNV        ;函数返回, 并且将栈顶的值作为返回值
0x19 GETL n(1b)     ;从局部存储取出数据入栈
0x1A SETL n(1b)     ;将栈顶元素绑定到局部存储
0x1B BUILTIN n(1b)  ;取出一个内置函数入栈
0xFF END            ;停止执行
```

## 常量池编码定义

```
0x00                ;空数据
0x01 INT l(1b) n(lb);整型数据
0x02 STR l(2b) m(lb);字符串数据, l指示了该字符串的长度
0xFF CUSTOM         ;自定义类型
```

## 内置函数定义

```
print
len
input
```
