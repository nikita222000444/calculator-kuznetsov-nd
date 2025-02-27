#include "skip.h"

int parse_num(char** ptr_) {
  if (!isdigit(**ptr_)) {
    printf("Digit expected but met %c\n", **ptr_);
    exit(1);
  }

  int res = 0;

  while (isdigit(**ptr_)) {
    res = res * 10 + (**ptr_ - '0');
    ++(*ptr_);
  }
  return res;
}

int calc_expression_int(char** ptr_);

int calc_factor_int(char** ptr_) {
  ignore_spaces(ptr_);
  if (**ptr_ == '(') {
    ++(*ptr_);
    int num = calc_expression_int(ptr_);
    ignore_spaces(ptr_);
    if (**ptr_ != ')') {
      printf("There is no \')\'\n");
      exit(1);
    }
    ++(*ptr_);
    return num;
  }
  return parse_num(ptr_);
}

int calc_term_int(char** ptr_) {
  int fac = calc_factor_int(ptr_);
  int next_fac;
  ignore_spaces(ptr_);
  char operation;
  while (**ptr_ == '*' || **ptr_ == '/') {
    operation = **ptr_;
    ++(*ptr_);
    next_fac = calc_factor_int(ptr_);
    ignore_spaces(ptr_);

    if (operation == '*')
      fac *= next_fac;
    else {
      if (next_fac != 0)
        fac /= next_fac;
      else {
        printf("Dividing by 0 is prohibited\n");
        exit(1);
      }
    }
  }
  return fac;
}

int calc_expression_int(char** ptr_) {
  int term = calc_term_int(ptr_);
  int next_term;
  ignore_spaces(ptr_);
  char operation;
  if (**ptr_ != '+' && **ptr_ != '-' && **ptr_ != '\0') {
    printf("Operation expected but met %c\n", **ptr_);
    exit(1);
  }
  while (**ptr_ == '+' || **ptr_ == '-') {
    operation = **ptr_;
    ++(*ptr_);
    next_term = calc_term_int(ptr_);
    ignore_spaces(ptr_);

    if (**ptr_ != '+' && **ptr_ != '-' && **ptr_ != '\0' && **ptr_ != ')') {
      printf("Operation expected but met %c\n", **ptr_);
      exit(1);
    }

    if (operation == '+')
      term += next_term;
    else
      term -= next_term;
  }
  return term;
}

float calc_expression_float(char** ptr_);

float calc_factor_float(char** ptr_) {
  ignore_spaces(ptr_);
  if (**ptr_ == '(') {
    ++(*ptr_);
    float num = calc_expression_float(ptr_);
    ignore_spaces(ptr_);
    if (**ptr_ != ')') {
      printf("There is no \')\'\n");
      exit(1);
    }
    ++(*ptr_);
    return num;
  }
  return parse_num(ptr_);
}

float calc_term_float(char** ptr_) {
  float fac = calc_factor_float(ptr_);
  float next_fac;
  ignore_spaces(ptr_);
  char operation;

  while (**ptr_ == '*' || **ptr_ == '/') {
    operation = **ptr_;
    ++(*ptr_);

    next_fac = calc_factor_float(ptr_);
    ignore_spaces(ptr_);

    if (operation == '*')
      fac *= next_fac;
    else {
      if (next_fac != 0)
        fac /= next_fac;
      else {
        printf("Dividing by 0 is prohibited\n");
        exit(1);
      }
    }
  }
  return fac;
}

float calc_expression_float(char** ptr_) {
  float term = calc_term_float(ptr_);
  float next_term;
  ignore_spaces(ptr_);
  char operation;

  if (**ptr_ != '+' && **ptr_ != '-' && **ptr_ != '\0') {
    printf("Operation expected but met %c\n", **ptr_);
    exit(1);
  }
  while (**ptr_ == '+' || **ptr_ == '-') {
    operation = **ptr_;
    ++(*ptr_);

    next_term = calc_term_float(ptr_);
    ignore_spaces(ptr_);

    if (**ptr_ != '+' && **ptr_ != '-' && **ptr_ != '\0' && **ptr_ != ')') {
      printf("Operation expected but met %c\n", **ptr_);
      exit(1);
    }

    if (operation == '+')
      term += next_term;
    else
      term -= next_term;
  }

  return term;
}
#ifndef GTEST
int main(int argc, char* argv[]) {
  printf("Enter the expression\n");
  char* expression = malloc(sizeof(char) * 1025);
  if (fgets(expression, sizeof(char) * 1025, stdin) == NULL) {
    printf("Expression is not expression\n");
    return 1;
  }

  char** ptr = &expression;
  if (argc == 1)
    printf("%d\n", calc_expression_int(ptr));
  else if (strcmp(argv[1], "--float") == 0)
    printf("%.4f\n", calc_expression_float(ptr));
  return 0;
}
#endif
