from sympy import *

class Instruction:
    def __init__(self, operation, register, parameter):
        self.operation = operation
        self.register = register
        if parameter:
            self.parameter = parameter

def parse_input(input):
    input = input.copy()
    instructions = []

    for line in input:
        line = line.strip('\n')
        instruction_parts = line.split(' ')
        instructions.append(
            Instruction(
                instruction_parts[0],
                instruction_parts[1],
                instruction_parts[2] if len(instruction_parts) > 2 else None
            )
        )

    return instructions


def part1(instructions):
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    idx = 0
    part1_result = 0

    def get_value(parameter):
        try:
            return int(parameter)
        except ValueError:
            return registers[parameter]
        
    while idx >= 0 and idx < len(instructions):

        instruction = instructions[idx]
        
        match instruction.operation:
            case 'set':
                registers[instruction.register] = get_value(instruction.parameter)
            case 'sub':
                registers[instruction.register] -= get_value(instruction.parameter)
            case 'mul':
                registers[instruction.register] *= get_value(instruction.parameter)
                part1_result += 1
            case 'jnz':
                current_register_value = get_value(instruction.register)
                if current_register_value != 0:
                    idx += get_value(instruction.parameter)
                    continue
        idx += 1

    return part1_result


def part2():
    # TLDR: This whole frickin' thing is counting composite numbers between 107900 and 124900 in increments of 17
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    registers['b'] = 107900
    registers['c'] = 107900 + 17000

    while True:
        registers['f'] = 1
        registers['d'] = 2

        # This loop is trying values from 0 to B and seeing if they divided B
        # I.E. is B prime?
        # while registers['d'] - registers['b'] != 0:
        #     registers['e'] = 2
            
        #     # this whole loop is checking if some value of E times D equals B
        #     # I.E. is computing if B is divisible by D
        #     # while registers['e'] - registers['b'] != 0:
        #     #     if (registers['d'] * registers['e']) - registers['b'] == 0: # This formula is checking if B is divisible by D
        #     #         registers['f'] = 0
        #     #     registers['e'] += 1
        #     if registers['b'] % registers['d'] == 0:
        #         registers['f'] = 0

        #     registers['d'] += 1

        if not isprime(registers['b']):
            registers['h'] += 1

        if registers['b'] == registers['c']:
            return registers['h']
        else:
            registers['b'] += 17


def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day23/input.txt', 'r').readlines()
    instructions = parse_input(input)

    # part 1
    part1_result = part1(instructions)
    print(f"Part 1: {part1_result}")

    # part 2
    part2_result = part2()
    print(f"Part 2: {part2_result}")


main()
