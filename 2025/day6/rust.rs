use std::fs;
use std::cmp::max;

fn part1(input: &Vec<&str>) -> u64 {
    // Parse input to values and operators
    let mut values: Vec<Vec<u64>> = Vec::new();
    let mut operators: Vec<char> = Vec::new();
    for row_idx in 0..input.len() {
        if row_idx == input.len() - 1 {
            operators = input[row_idx]
                .split_whitespace()
                .filter(|&op| op == "+" || op == "*")
                .map(|op| op.chars().next().unwrap())
                .collect();
        } else {
            let line_values: Vec<u64> = input[row_idx]
                .split_whitespace()
                .map(|val| val.parse().expect("Value is not numeric"))
                .collect();
            values.push(line_values);
        }
    }

    // Iterate column-wise and perform operations
    let mut result: u64 = 0;
    for col_idx in 0..operators.len() {
        let operator: char = operators[col_idx];

        // Initialize running_total to identity element for column's operation
        let mut running_total: u64 = 0;
        if operator == '*' {
            running_total = 1;
        }

        // Total up the column
        for row_idx in 0..values.len() {
            if operator == '*' {
                running_total *= values[row_idx][col_idx];
            } else {
                running_total += values[row_idx][col_idx];
            }
        }

        result += running_total;
    }

    return result;
}

fn part2(input: &Vec<&str>) -> u64 {
    let parsed_input: Vec<Vec<char>> = input
        .iter()
        .map(|row| row.chars().collect())
        .collect();

    let height: usize = parsed_input.len();
    let width: usize = parsed_input
        .iter()
        .map(|row| row.len())
        .max()
        .unwrap_or(0);

    let mut result: u64 = 0;
    let mut current_operation: char = '+';
    let mut running_total: u64 = 0;
    for col_idx in 0..width {
        // Check for new operator
        let operator_row_val: char = parsed_input[height - 1]
            .get(col_idx)
            .copied()
            .unwrap_or(' ');
        if operator_row_val != ' ' {
            // Update result with running total, reset operator, re-seed running total
            result += running_total;
            current_operation = operator_row_val;
            if current_operation == '+' {
                running_total = 0;
            } else {
                running_total = 1;
            }
        }

        // Build num for this column
        let mut current_num: u64 = 0;
        for row_idx in 0..height-1 {
            if let Some(char) = parsed_input[row_idx].get(col_idx) {
                if *char != ' ' {
                    let digit: u64 = char
                        .to_digit(10)
                        .expect("Value is not numeric") as u64;
                    current_num *= 10;
                    current_num += digit;
                }
            }
            
        }

        // Apply operation to running_total
        if current_operation == '+' {
            running_total += current_num;
        } else {
            running_total *= max(current_num, 1);
        }
    }

    result += running_total;
    return result;
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

    // Part 1 Example
    let part1_example_result = part1(&example_input_list);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&input_list);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_input_list);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&input_list);
    println!("Part 2: {}", part2_result);
}