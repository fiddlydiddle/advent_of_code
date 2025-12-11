from collections import deque

class MachineSchematic:
    def __init__(self, desired_state, button_config, joltage_limits):
        self.desired_state = desired_state
        self.button_config = button_config
        self.joltage_limits = joltage_limits

def part1(machine_schematics):
    result = 0
    for machine_schematic in machine_schematics:
        result += configure_lights(machine_schematic)

    return result


def configure_lights(machine_schematic):
    current_state = '.' * len(machine_schematic.desired_state)
    # Do BFS of all possible button presses until we reach desired_state
    queue = deque([(current_state, 0)])
    seen_states = set()
    while len(queue) > 0:
        current_state, depth = queue.popleft()
        if current_state not in seen_states:
            seen_states.add(current_state)
            depth += 1

            # Try all button presses on current state
            desired_state_found, queue = try_all_button_presses(machine_schematic, current_state, depth, queue)
            if desired_state_found:
                return depth


def try_all_button_presses(machine_schematic, current_state, depth, queue):
    for button_presses in machine_schematic.button_config:
        new_state = ''
        for idx, char in enumerate(current_state):
            if idx in button_presses:
                new_state += '.' if current_state[idx] == '#' else '#'
            else:
                new_state += char

            if new_state == machine_schematic.desired_state:
                print(f"Found: {new_state} at depth {depth}")
                return True, queue
            else:
                queue.append((new_state, depth))

    return False, queue

def parse_input(input):
    machine_schematics = []
    for line in input:
        opening_bracket_idx = line.index('[')
        closing_bracket_idx = line.index(']')
        desired_state = line[opening_bracket_idx+1:closing_bracket_idx]

        opening_curly_brace_idx = line.index('{')
        closing_curly_brace_idx = line.index('}')
        joltage_limits = line[opening_curly_brace_idx+1:closing_curly_brace_idx].split(',')
        joltage_limit_list = [0] * len(joltage_limits)
        for idx in range(len(joltage_limits)):
            joltage_limit_list[idx] = int(joltage_limits[idx])
       

        button_config = line[closing_bracket_idx+1:opening_curly_brace_idx-1].split()
        for idx in range(len(button_config)):
            button = button_config[idx]
            parsed_button = []
            lights = button[1:len(button)-1].split(',')
            for jdx in range(len(lights)):
                parsed_button.append(int(lights[jdx]))
            button_config[idx] = set(parsed_button)
        
        machine_schematics.append(MachineSchematic(desired_state, button_config, joltage_limit_list))

    return machine_schematics



def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    parsed_example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().split('\n')
    parsed_input = parse_input(input)

    # Part 1 Example
    part1_example_result = part1(parsed_example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(parsed_input)
    print(f"Part 1: {part1_result}")

main()