# YAMI: Yet, Antoher Monkey Interpreter

## What is monkey?

[Monkey](https://monkeylang.org) is a programming language invented by [Thorsten Ball](https://thorstenball.com) for his books [Writing an Interpreter in GO](https://interpreterbook.com) and [Writing a Compiler in GO](https://compilerbook.com).

I studied and appreciated the first one, so I made the interpreter in Python, planning to add some more features (>= 1.1). 

## How to use it

There are two ways to use monkey:
- REPL: exectuing the script `monkey.py` without arguments, you will get a prompt (`>>`) where you can write monkey code;
- file: if you specify a file path as an argument, you can execute it. Some examples are in `_Test/`.

## Changelog

**V. 1.2**: 
- Improved scopes' handling of name bindings;
- Literal float support;
- New operations between strings: `==` and `!=`;
- New builtin functions: 
    - `input`, to get input from stdin;
    - `int`, to convert an appropriate string to a numebr;
    - `printl`, to print a value and a new line;
- Classes and objects:
```c++
let Circle = class{
    let radius = 20;
    let PI = 3.14;

    let area = fn(){
        return radius * radius * PI
    }
}

let ca = Circle();
let cb = Circle();
printl(ca.area());        // -> 1256.0
let cb.radius = 100;
printl(cb.area());        // -> 31400.0
```


**V. 1.1**: 
- New operators: `%`, `and`, `&&`, `||`, `or`, `>=`, `<=`;
- Comments, both inline with `//` as multiline, `/* ... */`;
- If you already declared a variable using `let`, you can assign it a new value with the `=` operator;
- New builtin functions: 
    - `update`, to update an element of a value;
    - `str`, to convert an object into a string;
    - `exit`, to exit the program.
- While and for loops:
```c++
while(condition){
    statement[0];
    ...
    statement[n];
}

for({initial let statement};{end condition};{update statement}){
    statement[0];
    ...
    statement[n];
}
```
- `continue` and `break` for loops.

**V. 1.0**: 
The interpreter works with all the starting features presented in the book (variable, funcitons, if statements, strings, opeartors, array, hash and much more). 