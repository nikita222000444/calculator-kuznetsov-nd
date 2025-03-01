#include "skip.h"

void ignore_spaces(char** ptr_) {
  while (isspace(**ptr_) || **ptr_ == '\r' || **ptr_ == '\n' || **ptr_ == '\t' || **ptr_ == '\v')
    ++(*ptr_);
}
