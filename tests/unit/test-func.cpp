#include <gtest/gtest.h>

extern "C" {
void ignore_spaces(char** ptr_);
int parse_num(char** ptr_);
int calc_factor_int(char** ptr_);
int calc_term_int(char** ptr_);
int calc_expression_int(char** ptr_);
float calc_factor_float(char** ptr_);
float calc_term_float(char** ptr_);
float calc_expression_float(char** ptr_);
}

TEST(NonRecTests, SkipSpaces) {
  char str[] = "    l  ";
  char* temp = str;
  char** ptr = &temp;
  ignore_spaces(ptr);
  EXPECT_EQ(**ptr, 'l');
}

TEST(NonRecTests, ParseNumber) {
  char str[] = "100000+";
  char* temp = str;
  char** ptr = &temp;
  int num = parse_num(ptr);
  EXPECT_EQ(num, 100000);
}

TEST(RecTests, FacInt) {
  char str[] = " (( 11 + 3 * 3) + ( 4 - 1 )/ 3)";
  char* temp = str;
  char** ptr = &temp;
  int num = calc_factor_int(ptr);
  EXPECT_EQ(num, 21);

  char str2[] = " 11 + 3 * 3) + ( 4 - 1 )/ 3)";
  temp = str2;
  ptr = &temp;
  num = calc_factor_int(ptr);
  EXPECT_EQ(num, 11);
}

TEST(RecTests, TermInt) {
  char str[] = "11*7";
  char* temp = str;
  char** ptr = &temp;
  int num = calc_term_int(ptr);
  EXPECT_EQ(num, 77);

  char str2[] = "11/7";
  temp = str2;
  ptr = &temp;
  num = calc_term_int(ptr);
  EXPECT_EQ(num, 1);
}

TEST(RecTests, ExpInt) {
  char str[] = " 24344+56";
  char* temp = str;
  char** ptr = &temp;
  int num = calc_expression_int(ptr);
  EXPECT_EQ(num, 24400);

  char str2[] = "24344-44";
  temp = str2;
  ptr = &temp;
  num = calc_expression_int(ptr);
  EXPECT_EQ(num, 24300);
}

TEST(RecTests, FacFloat) {
  char str[] = " (( 11 + 3 * 3) + ( 4 - 1 )/ 3)";
  char* temp = str;
  char** ptr = &temp;
  float num = calc_factor_float(ptr);
  EXPECT_EQ(num, 21);

  char str2[] = " 11 + 3 * 3) + ( 4 - 1 )/ 3)";
  temp = str2;
  ptr = &temp;
  num = calc_factor_float(ptr);
  EXPECT_EQ(num, 11);
}

TEST(SkipTests, TermFloat) {
  char str[] = " 11 * 7";
  char* temp = str;
  char** ptr = &temp;
  float num = calc_term_float(ptr);
  EXPECT_EQ(num, 77);

  char str2[] = "11/7";
  temp = str2;
  ptr = &temp;
  num = calc_term_float(ptr);
  EXPECT_EQ(num, (float)11 / 7);
}

TEST(RecTests, ExpFloat) {
  char str[] = " 24344+56";
  char* temp = str;
  char** ptr = &temp;
  float num = calc_expression_float(ptr);
  EXPECT_EQ(num, 24400);

  char str2[] = "24344-44";
  temp = str2;
  ptr = &temp;
  num = calc_expression_float(ptr);
  EXPECT_EQ(num, 24300);
}
