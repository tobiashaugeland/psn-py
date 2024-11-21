# Variables
CXX = c++
CXXFLAGS = -O3 -Wall -shared -std=c++11 -fPIC
PYTHON_INCLUDES = $(shell python3-config --includes)
EXT_SUFFIX = $(shell python3-config --extension-suffix)
INCLUDES = -Ivendors/psn/include -Ivendors/pybind11/include
SRC = src/main.cpp
TARGET = psn$(EXT_SUFFIX)

# Build target
all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(PYTHON_INCLUDES) $(INCLUDES) $(SRC) -o $(TARGET)

# Clean target
clean:
	rm -f $(TARGET)

.PHONY: all clean
