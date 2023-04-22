#include <iostream>
#include <vector>
#include <fstream>

#include "lexer.hpp"
#include "token.hpp"

using namespace std;

string trim(const string &str) {
	const std::string whitespace = " \n\r\t\f\v";

	size_t start = str.find_first_not_of(whitespace);
	string lstripped = (start == string::npos) ? "" : str.substr(start);

	size_t end = lstripped.find_last_not_of(whitespace);
    return (end == string::npos) ? "" : lstripped.substr(0, end + 1);
}

int main() {
	string filepath = "tests/test.rks";

	ifstream reader(filepath);
	string line;
	while (getline(reader, line)) {
		vector<Token> tokens = lex(trim(line));

		for (Token token: tokens) {
			cout << "Token Type: " << token.type << "\nValue: " << token.value << endl;
		}
	}

	return 0;
}
