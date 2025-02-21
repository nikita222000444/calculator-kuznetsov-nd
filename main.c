#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>


void ignore_spaces(char** ptr_)
{
    while(isspace(**ptr_)) 
            ++(*ptr_);
}

int parse_num(char** ptr_)
{
    int res = 0;
    while(isdigit(**ptr_))
    {
        res = res * 10 + (**ptr_ - '0');
        ++(*ptr_);
    }
    return res;
}

int calc_expression(char** ptr_);

int calc_factor(char** ptr_)
{
    ignore_spaces(ptr_);
    if(**ptr_ == '(')
    {
        ++(*ptr_);
        int num = calc_expression(ptr_);
        ignore_spaces(ptr_);
        if(**ptr_ != ')')
        {
            printf("There is no \')\'\n");
            return 0;
        }
        ++(*ptr_);
        return num;
        
    }
    return parse_num(ptr_);
}

int calc_term(char** ptr_)
{
    int fac = calc_factor(ptr_);
    int next_fac;
    ignore_spaces(ptr_);
    char operation;
    while(**ptr_ == '*' || **ptr_ == '/')
    {
        operation = **ptr_;
        ++(*ptr_);
        next_fac = calc_factor(ptr_);
        ignore_spaces(ptr_);
        
        if(operation == '*') fac *= next_fac;
        else 
        {
            if(next_fac != 0) fac /= next_fac;
            else 
            {
                printf("Dividing by 0 is prohibited\n");
                return 0;
            }
        }  
    }
    return fac;
}

int calc_expression(char** ptr_)
{
    int term = calc_term(ptr_);
    int next_term;
    ignore_spaces(ptr_);
    char operation;
    while(**ptr_ == '+' || **ptr_ == '-')
    {
        operation = **ptr_;
        ++(*ptr_);
        next_term = calc_term(ptr_);
        ignore_spaces(ptr_);
        
        if(operation == '+') term += next_term;
        else term -= next_term;
        
    }
    return term;
}

int main() {
    char* expression = malloc(sizeof(char) * 1024);
    if (fgets(expression, sizeof(char) * 1024, stdin) == NULL) {
        printf("Expression is not expression\n");
        return 1;
    }
    char** ptr = &expression;
    printf("%d\n", calc_expression(ptr));
    
    return 0;
}
