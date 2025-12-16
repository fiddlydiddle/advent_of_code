import math

class MachineSchematic:
    def __init__(self, desired_binary_state: list[int], button_config: list[list[int]], desired_joltages: list[int]):
        self.desired_binary_state = desired_binary_state
        self.button_config = button_config
        self.desired_joltages = desired_joltages


def part2(machine_schematics: list[MachineSchematic]):
    result = 0
    for idx, machine_schematic in enumerate(machine_schematics):
        # Convert buttons from button config to vectors
        button_effects = []
        for button in machine_schematic.button_config:
            button_effect = [0] * len(machine_schematic.desired_joltages)
            for joltage_idx in button:
                button_effect[joltage_idx] = 1
            button_effects.append(button_effect)
        # Get all button combo parity effects
        button_combo_effects = dfs_button_combinations(
            machine_schematic.button_config,
            len(machine_schematic.desired_joltages),
            0,
            [0] * len(machine_schematic.button_config),
            {}
        )
        # DFS to find which button combo solves with minimum presses
        min_presses = dfs_compute_min_presses(
            tuple(machine_schematic.desired_joltages),
            button_effects,
            button_combo_effects,
        )
        # print(f"Machine {idx} min presses: {min_presses}")
        result += min_presses

    return result


def dfs_compute_min_presses(
    current_joltages,
    button_effects,
    button_combo_effects,
):
    if sum(current_joltages) == 0:
        return 0

    # Find parity pattern of current joltages
    # E.g. 3,5,4,7 -> 1,1,0,1
    required_pattern = [joltage % 2 for joltage in current_joltages]
    # Lookup button combos with a matching parity effect.
    # These button combos will make all joltage values even
    # E.g. button combo of 1,1,0,1 applied to above parity pattern of
    # 1,1,0,1 results in 0,0,0,0
    possible_combos = button_combo_effects.get(tuple(required_pattern), [])

    # Go through each combo and apply it if it's valid
    min_found = math.inf
    for button_press_combo in possible_combos:
        reduced_joltage = list(current_joltages)
        num_presses = 0

        # Apply button combo and see if it's valid (doesn't produce negative joltages)
        is_valid = True
        for idx in range(len(button_press_combo)):
            # Check if button is pressed in this combo
            if button_press_combo[idx] == 1:
                num_presses += 1
                button_effect = button_effects[idx]
                
                # Apply button effect to joltages
                for joltage_idx in range(len(current_joltages)):
                    if button_effect[joltage_idx] == 1:
                        reduced_joltage[joltage_idx] -= 1
                        # Make sure joltages don't go negative
                        if reduced_joltage[joltage_idx] < 0:
                            is_valid = False
                            break
                if not is_valid:
                    break
        
        # Skip invalid combos
        if not is_valid:
            continue

        # Remaining combos will make all joltages even
        # We can safely divide all the joltages by two and recurse
        reduced_joltage_tuple = tuple(x // 2 for x in reduced_joltage)
        min_from_here = dfs_compute_min_presses(
            reduced_joltage_tuple, 
            button_effects, 
            button_combo_effects
        )
        
        if min_from_here != math.inf:
            # Double the halved solution and add presses from current combo
            total_cost = (2 * min_from_here) + num_presses
            min_found = min(min_found, total_cost)

    return min_found

# DFS search to find all single-press combinations of buttons
# Returns a map of combo effect keys and values of combos which produce that effect
def dfs_button_combinations(
    button_config,
    num_joltages,
    next_button_press,
    current_combination,
    seen_combinations,
):
    # Check if we've hit bottom (last button)
    if next_button_press == len(button_config):
        final_state = [0] * num_joltages
        for idx in range(len(button_config)):
            if current_combination[idx] == 1:
                # Apply the effect of button
                for joltage_idx in button_config[idx]:
                    final_state[joltage_idx] = 1 - final_state[joltage_idx]
                    
        # Record the result
        seen_combinations.setdefault(tuple(final_state), []).append(current_combination)
        return seen_combinations

    # Branch where we push this button and move to next
    new_combination = current_combination[:]
    new_combination[next_button_press] = 1
    dfs_button_combinations(
        button_config,
        num_joltages,
        next_button_press + 1,
        new_combination,
        seen_combinations
    )

    # Branch where we don't push this button and move to next
    dfs_button_combinations(
        button_config,
        num_joltages,
        next_button_press + 1,
        current_combination,
        seen_combinations
    )

    return seen_combinations   

def parse_input(input):
    machine_schematics = []
    for line in input:
        # Parse binary states
        opening_bracket_idx = line.index('[')
        closing_bracket_idx = line.index(']')
        desired_binary_state = line[opening_bracket_idx+1:closing_bracket_idx]

        # Parse joltages
        opening_curly_brace_idx = line.index('{')
        closing_curly_brace_idx = line.index('}')
        joltage_limits = line[opening_curly_brace_idx+1:closing_curly_brace_idx].split(',')
        desired_joltages = [0] * len(joltage_limits)
        for idx in range(len(joltage_limits)):
            desired_joltages[idx] = int(joltage_limits[idx])
       
        # Parse buttons
        button_config = line[closing_bracket_idx+1:opening_curly_brace_idx-1].split()
        for idx in range(len(button_config)):
            button = button_config[idx]
            parsed_button = []
            lights = button[1:len(button)-1].split(',')
            for jdx in range(len(lights)):
                parsed_button.append(int(lights[jdx]))
            button_config[idx] = parsed_button
        
        machine_schematics.append(MachineSchematic(desired_binary_state, button_config, desired_joltages))

    return machine_schematics

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    parsed_example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().split('\n')
    parsed_input = parse_input(input)

    # Part 2 Example (Correct answer: 33)
    part2_example_result = part2(parsed_example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2 (Correct answer: 19293)
    part2_result = part2(parsed_input)
    print(f"Part 2: {part2_result}")

main()
