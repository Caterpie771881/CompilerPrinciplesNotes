# SimpleRegexEngine

## 简介

一个用于学习编译原理的简单正则引擎, 基于 DFA, 使用原生 python 实现

内含:
1. 自定义的 NFA 和 DFA 结构 (可以直接转换为对应的五元组)

2. 能够将合法正则表达式字符串编译为 NFA 的简易编译器

3. 使用子集构造算法的 NFA 到 DFA 转换器

4. 使用 hopcroft 算法的 DFA 到 "最小化DFA" 转换器 

## 支持的语法

支持原始正则表达式的全部语法

- [x] 匹配单个字符
- [x] `AB` 连接运算, 先匹配 A 然后匹配 B
- [x] `A|B` 并运算, 匹配 A 或 B
- [x] `A*` 求表达式 A 的闭包, 也就是匹配 A 零次到无穷次
- [x] `(A)` 优先计算括号内的表达式

支持一些语法糖

- [x] `A?` 等价于 `ε|A`, 匹配 A 零次或一次
- [x] `A+` 等价于 `AA*`, 匹配 A 一次或无穷次
- [x] 使用 `.` 匹配单个任意字符

暂时不支持非贪婪匹配

不支持捕获组和反向引用

## 关于 Compiler

部分本科教材中使用中缀表达式转后缀表达式的方式实现 compiler

为了更好地扩展引擎支持的正则语法, 也为了复习编译原理的知识, 本项目没有沿用这种方法

而是通过词法分析和语法分析来实现 compiler

内含:

1. 使用手动分析实现的 Lexer

2. 使用递归向下分析实现的 Parser

3. 直接解释抽象语法树, 将 AST 转换为 NFA 的 NFABuilder

## 使用例

`SimpleRegexEngine` 提供了一些常用的 API

```python
import SimpleRegexEngine as sre

regex = r"a(b|c)*"

print(sre.match(regex, "abbcc"))            # 'abbcc'
print(sre.find(regex, "123abc456"))         # 'abc'
print(sre.findall(regex, "ab_ac_abc"))      # ['ab', 'ac', 'abc']
print(sre.sub(regex, 'hello', '123abc456')) # '123hello456'
print(sre.split(regex, '123abc456'))        # ['123', '456']
```

`SimpleRegexEngine` 构建的 NFA 和 DFA 都能以五元组的形式输出

```python
import SimpleRegexEngine as sre

regex = r"a(b|c)"

dfa = sre.compile(regex)
print(dfa)
# S: {0, 1, 2}
# ∑: {'a', 'b', 'c'}
# s0: 0
# F: {2}
# M: {0: {'a': 1}, 1: {'c': 2, 'b': 2}, 2: {}}
```

## TODO

- [ ] 添加懒惰模式的运算符
- [ ] 添加使用文档
