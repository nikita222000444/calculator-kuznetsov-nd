# calculator-kuznetsov-nd
A program written in C. It reads an arithmetic expression from standard input, parses it, and prints the result. The program supports the following operators on integers: `+` , `-` , `*` , `/` , `(` , and `)` . Any whitespace characters are allowed in input. 

Program does not provide any prompt to user — just reading input until `EOF`.
 
The input is shorter that 1KiB, all numbers are non negative integers fit into `int` type at any stage of evaluation.
 
Program outputs only a number. The whole program fits single `main.c` file. No any external dependencies are used except `libc`. 
