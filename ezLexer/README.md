# ezLexer

## 简介

一个使用正则表达式驱动的简易词法分析器, 使用 python 实现

目标是解析下面的语言规则

|词法类型|规则|
|--|--|
|关键字|if, else, true, false|
|标识符|以大小写字母、数字、下划线组成, 不能以数字开头|
|整数|由0-9组成, 多位数字不能以0开头|
|运算符|+, -, *, /, ==, >, <|

写嗨了, 词法单元得有点多, 后面将目标语言的语法规定一下再更新上面的表格

## 使用例

```python
from ezLexer import Lexer

source_code = "enter your src here"
lexer = Lexer(source_code)

for token in lexer.token_stream:
    print(token)
```

