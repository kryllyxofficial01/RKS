#ifndef ASSEMBLER
#define ASSEMBLER

#include <iostream>
#include <vector>
#include <algorithm>

#include "utils.hpp"
#include "token.hpp"
#include "error.hpp"

Instruction assemble(std::vector<Token> tokens, Error error);

#endif