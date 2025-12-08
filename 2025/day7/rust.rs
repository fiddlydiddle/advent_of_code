use std::fs;
use std::collections::HashMap;

struct SimulationResult {
    part1_result: u32,
    part2_result: u64
}

// Port of algorithm from python.py
fn part2(input: &Vec<&str>) -> SimulationResult {
    let parsed_input: Vec<Vec<char>> = input
        .iter()
        .map(|row| row.chars().collect())
        .collect();

    let mut beam_cols: HashMap<usize, u64> = HashMap::new();
    let mut part1_result: u32 = 0;

    // Find entry point in first row
    match input[0].find('S') {
        Some(index) => beam_cols.insert(index, 1),
        None => panic!("Couldn't find starting point")
    };

    for row_idx in 0..input.len() {
        let mut beams_to_add: Vec<(usize, u64)> = Vec::new();
        let mut beams_to_remove: Vec<usize> = Vec::new();

        for col_idx in beam_cols.keys() {
            if let Some(char) = parsed_input[row_idx].get(*col_idx) {
                if *char == '^' {
                    part1_result += 1;
                    let num_beams = beam_cols.get(col_idx).unwrap_or(&1);
                    beams_to_add.push((*col_idx - 1, *num_beams));
                    beams_to_add.push((*col_idx + 1, *num_beams));
                    beams_to_remove.push(*col_idx);
                }
            }
        }

        for beam_col in beams_to_remove {
            beam_cols.remove(&beam_col);
        }
        for beam_info in beams_to_add {
            *beam_cols.entry(beam_info.0).or_insert(0) += beam_info.1;
        }
    }

    return SimulationResult {
        part1_result: part1_result,
        part2_result: beam_cols.values().sum()
    };
}

fn part2_recursive(input: &Vec<&str>) -> u64 {
    let height = input.len();
    
    let first_beam_col = input[0]
        .find('S')
        .expect("Couldn't find starting point 'S'") as usize;

    // Map of coordinates and number of paths that lead there
    let mut memo: HashMap<(usize, usize), u64> = HashMap::new();

    return dfs(1, first_beam_col, input, height, &mut memo);
}

fn dfs(
    row_idx: usize,
    col_idx: usize,
    input: &Vec<&str>,
    height: usize,
    memo: &mut HashMap<(usize, usize), u64>,
) -> u64 {
    // Check if we've hit the bottom
    if row_idx == height {
        return 1;
    }

    // Check if we've been here before
    let key = (row_idx, col_idx);
    if let Some(&result) = memo.get(&key) {
        return result;
    }

    // Drill baby, drill
    let current_char = input[row_idx].chars().nth(col_idx).unwrap_or('.');
    let result = if current_char == '^' {
        let left_paths = dfs(row_idx + 1, col_idx - 1, input, height, memo);
        let right_paths = dfs(row_idx + 1, col_idx + 1, input, height, memo);
        left_paths + right_paths
    } else {
        dfs(row_idx + 1, col_idx, input, height, memo)
    };

    // Memoize and Return
    memo.insert(key, result);
    result
}

fn main() {
    // Example input
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_input_list: Vec<&str> = example_input.trim().split('\n').collect();

    // Input
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_list: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 & 2 Examples
    let example_result: SimulationResult = part2(&example_input_list);
    println!("Part 1 (example): {}", example_result.part1_result);
    println!("Part 2 (example): {}", example_result.part2_result);

    // Part 1 & 2
    let result: SimulationResult = part2(&input_list);
    println!("Part 1: {}", result.part1_result);
    println!("Part 2: {}", result.part2_result);

    // Part 2 (Recursive)
    let part2_recursive_result = part2_recursive(&input_list);
    println!("Part 2 (Recursive): {}", part2_recursive_result);
}