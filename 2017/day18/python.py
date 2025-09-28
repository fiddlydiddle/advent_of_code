import asyncio
from collections import deque

class Instruction:
    def __init__(self, operation, register, parameter):
        self.operation = operation
        self.register = register
        if parameter:
            self.parameter = parameter

class Program:
    def __init__(self, program_id):
        self.program_id = program_id

        self.registers = { 'p': program_id }

        self.queue = deque()
        self.is_receiving = False
        self.messages_sent = 0

async def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day18/input.txt', 'r').readlines()
    instructions = parse_input(input)
    print(await part2(instructions))


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


async def part2(instructions):
    program0 = Program(0)
    program1 = Program(1)
    result = await run_programs(instructions, program0, program1)

    return f"Part 2: {result}"

    
async def run_programs(instructions: list[Instruction], program_0: Program, program_1: Program):
    program0_execution = asyncio.create_task(run_program(program_0, instructions, program_1))
    program1_execution = asyncio.create_task(run_program(program_1, instructions, program_0))

    deadlock_counter = 0
    while True:
        await asyncio.sleep(0.001)

        deadlock = (program_0.is_receiving and not program_0.queue) and \
                   (program_1.is_receiving and not program_1.queue)
        
        if deadlock:
            deadlock_counter += 1 
            
            if deadlock_counter >= 50: 
                program0_execution.cancel()
                program1_execution.cancel()
                break
        else:
            deadlock_counter = 0 

    await asyncio.gather(program0_execution, program1_execution, return_exceptions=True)
    return program_1.messages_sent
            
    
async def run_program(program: Program, instructions: list[Instruction], other_program: Program):
    try:
        idx = 0
        iteration = 0
        most_recent_sound = None
        part1_result = None

        def get_value(parameter):
            try:
                return int(parameter)
            except ValueError:
                return program.registers[parameter]
            
        while idx >= 0 and idx < len(instructions):
            # Periodically free up the thread so the other program can run too
            if iteration % 100 == 0:
                await asyncio.sleep(0)

            instruction = instructions[idx]
            if instruction.register not in program.registers:
                program.registers[instruction.register] = 0
            
            match instruction.operation:
                case 'snd':
                    # For part 1
                    register_value = program.registers[instruction.register]
                    most_recent_sound = register_value 
                    # For part 2
                    other_program.queue.append(register_value)
                    program.messages_sent += 1
                case 'set':
                    program.registers[instruction.register] = get_value(instruction.parameter)
                case 'add':
                    program.registers[instruction.register] += get_value(instruction.parameter)
                case 'mul':
                    program.registers[instruction.register] *= get_value(instruction.parameter)
                case 'mod':
                    value = get_value(instruction.parameter)
                    if value > 0:
                        program.registers[instruction.register] %= get_value(instruction.parameter)
                case 'rcv':
                    program.is_receiving = True

                    # For Part 1
                    if program.registers[instruction.register] != 0 and not part1_result and program.program_id == 0:
                        part1_result = most_recent_sound
                        print(f"Part 1: {part1_result}")

                    # For Part 2
                    while program.is_receiving:
                        if len(program.queue) > 0:
                            new_value = program.queue.popleft()
                            program.registers[instruction.register] = new_value
                            program.is_receiving = False
                        else:
                            await asyncio.sleep(0.001)
                case 'jgz':
                    if get_value(instruction.register) > 0:
                        idx = idx + get_value(instruction.parameter)
                        continue

            idx += 1
            iteration += 1

        print(f"Program {program.program_id} done")
    except Exception as ex:
        print(f"Exception {ex}")

asyncio.run(main())
