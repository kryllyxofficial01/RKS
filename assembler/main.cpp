#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <filesystem>

#include "lexer.hpp"
#include "assembler.hpp"
#include "token.hpp"
#include "error.hpp"
#include "instruction.hpp"

#define WHITESPACE " \n\r\t\f\v"

using namespace std;

string trim(const string &str) {
	size_t start = str.find_first_not_of(WHITESPACE);
	string lstripped = (start == string::npos) ? "" : str.substr(start);

	size_t end = lstripped.find_last_not_of(WHITESPACE);
    return (end == string::npos) ? "" : lstripped.substr(0, end + 1);
}

int main() {
	string filepath = "tests/test.rks";
	vector<Instruction> instructions;

	ifstream reader(filepath);
	string line;
	int lineno = 1;
	while (getline(reader, line)) {
		instructions.push_back((Instruction) {
			.line = trim(line),
			.lineno = lineno,
			.file = filesystem::absolute(filepath)
		});

		lineno++;
	}

	for (Instruction instruction: instructions) {
		Error error(
			instruction.line,
			instruction.lineno,
			instruction.file
		);
		vector<Token> tokens = lex(instruction, error);

		assemble(tokens, instruction.file, error);
	}

	return 0;
}
