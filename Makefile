# Tools
CC  ?= gcc
CXX ?= g++
AR  ?= ar

# Google Test root directory
GTEST_DIR = googletest/googletest
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

#Python
PYTHON := python3
PIP := pip3
VENV_NAME := venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
VENV_PYTHON := $(VENV_NAME)/bin/python
VENV_PIP := $(VENV_NAME)/bin/pip
PYTEST := $(VENV_NAME)/bin/pytest

APP_BUILD_DIR=build/app
TEST_BUILD_DIR=build/test

TEST_BUILD_DIR_APP_OBJS=$(TEST_BUILD_DIR)/app
TEST_BUILD_DIR_UNIT_TESTS_OBJS=$(TEST_BUILD_DIR)/unit-tests

# Flags
CPPFLAGS += -isystem $(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -pthread -std=c++17
CFLAGS   += -g -Wall -Wextra -Wpedantic -Werror -std=c11

SRC_DIR=src
TESTS_DIR=tests
BUILD_DIR=build

# Find all C source files recursively
APP_SRCS := $(shell find $(SRC_DIR) -name '*.c')

# Find all test files inside the tests directory
TEST_SRCS := $(shell find $(TESTS_DIR) -name '*.cpp')

# Generate object file paths
APP_OBJS := $(patsubst $(SRC_DIR)/%.c, $(APP_BUILD_DIR)/%.o, $(APP_SRCS))
TEST_OBJS := $(patsubst $(SRC_DIR)/%.c, $(TEST_BUILD_DIR_APP_OBJS)/%.o, $(APP_SRCS))
UNIT_TESTS_OBJS := $(patsubst $(TESTS_DIR)/%.cpp, $(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o, $(TEST_SRCS))

# Create necessary build directories
$(shell mkdir -p $(APP_BUILD_DIR) $(TEST_BUILD_DIR))

################
# MAIN TARGETS #
################

# Housekeeping targets
all: $(BUILD_DIR)/app.exe $(BUILD_DIR)/unit-tests.exe

clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(VENV_NAME)

# Run the normal C application
run-int: $(BUILD_DIR)/app.exe
	@$<

# Run the normal C application with floating point numbers
run-float: $(BUILD_DIR)/app.exe
	@$< --float

# Run all tests
run-unit-tests: $(BUILD_DIR)/unit-tests.exe
	@$<

run-server: $(BUILD_DIR)/app.exe
	$(PYTHON) server/server.py || pip install structlog

run-gui: 
	$(PYTHON) gui/gui.py || pip install pyside6
	
#############
# BUILD APP #
#############

# Compile normal C application files (without -DGTEST)
-include $(APP_OBJS:.o=.d)
$(APP_BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

# Link the normal C application
$(BUILD_DIR)/app.exe: $(APP_OBJS)
	$(CC) $(CFLAGS) $^ -o $@
	
###############
# BUILD TESTS #
###############

# Compile test version of C application files (with -DGTEST)
-include $(TEST_OBJS:.o=.d)
$(TEST_BUILD_DIR_APP_OBJS)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -DGTEST -c $< -o $@

# Compile each C++ test source file into an object file (always with -DGTEST)
-include $(UNIT_TESTS_OBJS:.o=.d)
$(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o: $(TESTS_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

# Link test executable with the TEST version of the C application and gtest
$(BUILD_DIR)/unit-tests.exe: $(TEST_OBJS) $(UNIT_TESTS_OBJS) $(TEST_BUILD_DIR)/gtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -lpthread $^ -o $@
	
###########
# PYTESTS #
###########

# Create virtual environment if it doesn't exist
venv: 
	@$(PYTHON) -m venv $(VENV_NAME) || (echo "python3-venv not found. Installing..." && sudo apt update && sudo apt install python3.8-venv)

run-integration-tests: build/app.exe install-deps
	source $(VENV_NAME)/bin/activate; $(PYTEST) tests/integration/inttest.py
	

# Install dependencies in virtual environment
install-deps: venv
	@echo "Installing dependencies..."
	@. $(VENV_ACTIVATE) && $(VENV_PIP) install --upgrade pip
	@. $(VENV_ACTIVATE) && $(VENV_PIP) install pytest

####################################
# BUILD GOOGLE TEST STATIC LIBRARY #
####################################

# Google Test object files
$(TEST_BUILD_DIR)/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

$(TEST_BUILD_DIR)/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

# Google Test static libraries
$(TEST_BUILD_DIR)/gtest_main.a: $(TEST_BUILD_DIR)/gtest-all.o $(TEST_BUILD_DIR)/gtest_main.o
	$(AR) $(ARFLAGS) $@ $^ -o $@
