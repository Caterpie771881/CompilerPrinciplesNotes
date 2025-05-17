# SimpleParsers

基于 python 的简单语法分析器集合, 借用 ezLexer 包进行词法分析

也包含了语法制导翻译的过程, 将会输出抽象语法树

共用 ast.py 定义抽象语法树

## 语言特性

- 语句后以 ; 或 \} 结束
- 使用 : 进行类型标注
- 使用 {} 进行作用域标定
- 函数为一等公民
- 作用域闭包
- 使用 -> 标注函数返回值类型

内置类型: 标注 * 的为引用类型
- int
- float
- str
- bytes
- bool
- list*
- dict*
- func*
- module*
- nil
- set*

语句:
- 表达式语句
- 赋值语句 foo = bar
- 导入语句 import foo \[as bar\]
- 返回语句 return \[foo\]
- 流程控制语句 break, continue, pass
- 函数定义语句 def foo(...){...}
- 类型定义语句 class foo(...){...}

表达式:
- 整型、浮点型表达式
- 字符串表达式 "foo" 'bar'
- 列表表达式 \[foo, bar\]
- 字典表达式 {foo: bar}
- 集合表达式 {foo, bar}
- 布尔表达式 true false
- None 表达式 nil
- 表达式组 (foo)
- 函数表达式 fn(...){...}
- 标识符表达式 foo
- 条件表达式 if elif else
- 取下标表达式 foo\[bar\]
- 算数运算表达式 
    1. \+
    2. \-
    3. \*
    4. /
    5. %
- 逻辑运算表达式
    1. and &&
    2. or ||
    3. not !
    4. ==
    5. !=
    6. \>
    7. <
- 位运算表达式
    1. &
    2. |
    3. ~
    4. ^
- 函数调用表达式 foo(bar)
- 取属性表达式 foo.bar

使用例1
```
import time as t

calc_time: func = fn(task: func) -> float {
    start_time: int = t.time();
    task();
    return t.time() - start_time;
}

fib: func = fn(n: int) -> int | nil {
    if (n <= 0) {
        return nil;
    }
    if (n == 1 or n == 2) {
        return 1;
    } else {
        return fib(n-1) + fib(n-2);
    }
}

rem: list[int] = [1, 1]
def fib2(n: int) -> int | nil {
    if (n <= 0) {
        return nil;
    }
    if (n >= len(rem)) {
        return rem[n+1];
    } else {
        result: int = fib2(n-1) + fib2(n-2);
        rem.append(result);
        return result;
    }
}

time1: float = calc_time(fn() {
    fib(20);
});
print($"cost {time1:6f}s");

time2: float = calc_time(fn() {
    fib2(20);
})
print($"cost {time2:6f}s");
```

使用例2
```
class Person() {
    def __init__(self: Person, name: str = '') -> nil {
        self.name = name;
    }
    def sayHi(self: Person) -> nil {
        print($"{self.name} say: Hi!");
    }
}

class Student(Person) {
    def __init__(
        self: Student,
        name: str = '',
        id: int = -1,
    ) -> nil {
        super(self).__init__(name);
        self.id = id;
    }
}

mike: Person = Student(name='mike', id=123);
mike.sayHi();
```

## 运算符优先级定义

思考中...

## TODO

- [ ] 完善 AST 定义
- [ ] 规定运算符优先级
- [ ] 完成 Pratt 语法分析器
- [ ] 完成 LL(1) 语法分析器
- [ ] 完成 LR(0) 语法分析器
