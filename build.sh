BUILD=build

assemble() {
	mkdir -p $BUILD
	mkdir -p $BUILD/rks

	g++ rks/main.cpp rks/lexer.cpp rks/error.cpp -o $BUILD/rks/main
	./$BUILD/rks/main
}

set -e
assemble
