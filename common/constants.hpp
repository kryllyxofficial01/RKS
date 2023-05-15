#ifndef CONSTANTS
#define CONSTANTS

#include <vector>
#include <string>

#define WHITESPACE " \n\r\t\f\v"

const inline std::vector<std::string> MNEUMONICS = {
    "nop", "mov", "stw", "ldw", "psh", "pop",
    "add", "and", "or", "not", "jnz", "hlt"
};

const inline std::vector<std::string> REGISTER_IDS = {
    "a", "b", "c", "d", "f", "sp", "pc"
};

#endif