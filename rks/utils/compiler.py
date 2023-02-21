from .error import *

class Compiler:
	instructions = {
		"nop": (0, 0),
		"lda": (1, 1),
		"ldb": (2, 1),
		"ldc": (3, 1),
		"ldd": (4, 1),
		"swp": (5, 2),
		"mov": (6, 2),
		"sta": (7, 1),
		"stb": (8, 1),
		"stc": (9, 1),
		"std": (10, 1),
		"lra": (11, 1),
		"lrb": (12, 1),
		"lrc": (13, 1),
		"lrd": (14, 1),
		"psh": (15, 1),
		"pop": (16, 2),
		"add": (17, 2),
		"sub": (18, 2),
		"mul": (19, 2),
		"div": (20, 2),
		"and": (21, 2),
		"or": (22, 2),
		"nor": (23, 2),
		"xor": (24, 2),
  		"not": (25, 1),
		"inc": (26, 1),
		"dec": (27, 1),
		"cmp": (28, 2),
		"jmp": (29, 1),
		"jz": (30, 1),
		"jnz": (31, 1),
		"jn": (32, 1),
		"jnn": (33, 1),
		"jo": (34, 1),
		"jno": (35, 1),
		"out": (36, 1),
		"put": (37, 1),
		"hlt": (38, 1)
	}
	registers = {
		"a": 0,
		"b": 1,
		"c": 2,
		"d": 3,
		"f": 4,
		"pc": 5
	}

	def __init__(self, instruction: str, labels: dict[str, tuple[int, list[str]]], variables: dict[str, int], lines: list[str], error: Error) -> None:
		self.instruction = instruction
		self.labels = labels
		self.variables = variables
		self.lines = lines
		self.error = error

	def compile(self) -> list[str]:
		binary = []
		start = 1
		word = ""

		if self.instruction.startswith("#"):
			return binary

		instruction = [i.strip().lower() for i in self.instruction.split(" ")]
		instruction_idx = self.lines.index(self.instruction)

		try:
			print(f"Current Instruction: {instruction[0]} -> {'0'*(6-len(bin(self.instructions[instruction[0]][0])[2:])) + bin(self.instructions[instruction[0]][0])[2:]}")
		except KeyError:
			self.error.print_stacktrace("InstructionError", f"Unknown instruction '{instruction[0]}'")

		if len(instruction[1:]) <= self.instructions[instruction[0]][1]:
			binary.append("0"*(6-len(bin(self.instructions[instruction[0]][0])[2:])) + bin(self.instructions[instruction[0]][0])[2:])

			for arg in instruction[1:]:
				argBin = ""
				if arg[0] == "!":
					if arg[1:].isnumeric():
						argBin = "0"*(10-len(bin(int(arg[1:]))[2:])) + bin(int(arg[1:]))[2:]
					else:
						self.error.print_stacktrace("ValueError", f"Invalid immediate '{arg[1:]}'")

				elif arg[0] == "@":
					if arg[1:] in self.registers.keys():
						argBin = "0"*(10-len(bin(self.registers[arg[1:]])[2:])) + bin(self.registers[arg[1:]])[2:]
					else:
						self.error.print_stacktrace("RegisterError", f"Unknown register ID '{arg[1:]}'")

				elif arg[0] == "0":
					base = arg[1]
					start = 0
					if base == "b":
						try:
							temp = int(arg[2:], 2)
						except ValueError:
							self.error.print_stacktrace("ValueError", f"'{arg[2:]}' is not valid binary")
						else:
							argBin = "0"*(10-len(bin(temp)[2:].lstrip("0"))) + bin(temp)[2:].lstrip("0")

					elif base == "x":
						try:
							temp = int(arg[2:].lower(), 16)
						except ValueError:
							self.error.print_stacktrace("ValueError", f"'{arg[2:]}' is not valid hexadecimal")
						else:
							argBin = "0"*(10-len(bin(temp)[2:].lstrip("0"))) + bin(temp)[2:].lstrip("0")

					else:
						self.error.print_stacktrace("ArgError", f"Unknown base '{arg[0:2]}'")

				elif arg[0] == ".":
					try:
						for label in self.labels.keys():
							if self.labels[label][0] > instruction_idx:
								self.labels[label] = (self.labels[label][0]+1, self.labels[label][1],)
        
						word = "0"*(16-len(bin(self.labels[arg[1:]][0])[2:])) + bin(self.labels[arg[1:]][0])[2:]
						argBin = "0"*10

					except KeyError: self.error.print_stacktrace("LabelError", f"Unknown label '{arg[1:]}'")
				
				elif arg[0] == "$":
					argBin = "0"*(10-len(bin(self.variables[arg[1:]])[2:])) + bin(self.variables[arg[1:]])[2:]
				
				elif arg[0] == "'":
					if arg[-1] == "'":
						char = arg[1:-1]
						if len(char) == 1:argBin = "0"*(10-len(bin(ord(char))[2:])) + bin(ord(char))[2:]
						else: self.error.print_stacktrace("CharError", f"Expected 1 character, but found {len(char)}")

					else: self.error.print_stacktrace("CharError", "Missing closing \"'\"")

				else:
					self.error.print_stacktrace("ArgError", f"Unknown argument prefix '{arg[0]}'")

				if len(argBin) > 10:
					self.error.print_stacktrace("ValueError", f"Argument bit width goes over 10-bit limit: '{arg[start:]}' -> '{argBin}'")

				binary.append(argBin)

			if len(binary[1:]) == 2:
				args = binary[1:]
				for i in range(len(args)):
					args[i] = "0"*(5-len(args[i].lstrip("0"))) + args[i].lstrip("0")

				binary = list(binary[0]) + args

		else:
			extra = ", ".join([f"'{arg}'" for arg in instruction[1:][-(len(instruction[1:]) - self.instructions[instruction[0]][1]):]])
			self.error.print_stacktrace("ArgError", f"Extra arguments {extra}")
   
		if len(binary) == 1:
			binary.append("0"*10)

		return (binary + ["\n" + word]) if word else binary

	@classmethod
	def clean(cls, instructions: list[str]) -> list[str]:
		for i in range(len(instructions)):
			if instructions[i] == "\n" or instructions[i].strip().startswith(";"): instructions[i] = ""
			else: instructions[i] = instructions[i].rstrip()
		return instructions

	@classmethod
	def collect(cls, lines: list[str], location: str) -> tuple[dict[str, tuple[int, list[str]]], list[str]]:
		labels = {}
		instructions = []

		inLabel = False
		labelName = ""

		idx = -3 # For some reason this is offset by three
		for i in range(len(lines)):
			if lines[i].startswith("."):
				header = [temp.strip().lower() for temp in lines[i][1:].split(" ")]
				if header[0] == "label":
					labels[header[1]] = (idx, [])
					inLabel = True
					labelName = header[1]

				else: Error(lines[i], i+1, location).print_stacktrace("HeaderError", f"Unknown header type '{header[0]}'")

			elif lines[i] != "":
				if inLabel:
					if lines[i].replace("    ", "\t").startswith("\t"):
						labels[labelName][1].append(lines[i].strip())
					else: inLabel = False

				instructions.append(lines[i])
				idx += 1

		return labels, instructions
	
	@classmethod
	def getValue(cls, content: str) -> int:
		value = 0
		if content[0] == "!":
			try: value = int(content[1:])
			except ValueError: raise ImmediateValueError

		elif content[0] == "0":
			base = content[1]
			if base == "b":
				try: value = int(content[2:], base=2)
				except ValueError: raise BaseValueError
			
			elif base == "x":
				try: value = int(content[2:], base=16)
				except ValueError: raise BaseValueError
			
			else: raise BaseTypeError

		elif content[0] == "'":
			if content[-1] == "'":
				if len(content[1:-1]) == 1: value = ord(content[1:-1])
				else: raise CharContentError
			else: raise CharTerminationError
		
		else: raise PrefixError
		
		return value