use std::fs;

// Port of Python solution from python.py
struct ParsedInput {
    ranges: Vec<(u64, u64)>,
    ingredients: Vec<u64>
}

fn part1(input: &ParsedInput) -> u64 {
    let mut result: u64 = 0;

    for ingredient in &input.ingredients {
        let has_match: bool = input.ranges
            .iter()
            .any(|&(low_val, high_val)| low_val <= *ingredient && *ingredient <= high_val);

        if has_match {
            result += 1;
        }
    }

    return result;
}

fn part2(input: &ParsedInput) -> u64 {
    let mut sorted_ranges = input.ranges.clone();
    sorted_ranges
        .sort_by(|tuple1, tuple2| tuple1.0.cmp(&tuple2.0));

    let mut result: u64 = 0;

    let mut low_val: u64 = sorted_ranges[0].0;
    let mut high_val: u64 = sorted_ranges[0].0;

    for idx in 1..sorted_ranges.len() {
        let currrent_range: (u64, u64) = sorted_ranges[idx];
        let previous_range: (u64, u64) = sorted_ranges[idx - 1];

        if currrent_range.0 <= previous_range.1 {
            high_val = std::cmp::max(currrent_range.1, previous_range.1);
        } else {
            result += high_val - low_val + 1;
            low_val = currrent_range.0;
            high_val = currrent_range.1;
        }
    }

    result += high_val - low_val + 1;
    return result;
}

fn preprocess_input(input: &Vec<&str>) -> ParsedInput {
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    let mut ingredients: Vec<u64> = Vec::new();
    let mut parsing_ranges: bool = true;

    for line in input {
        if line.is_empty() {
            parsing_ranges = false;
            continue;
        }

        if parsing_ranges {
            let range_values: Vec<&str> = line.split('-').collect();
            let low_val: u64 = range_values[0].parse().expect("Value is not numeric");
            let high_val: u64 = range_values[1].parse().expect("Value is not numeric");
            ranges.push((low_val, high_val));
        }
        else {
            let ingredient: u64 = line.parse().expect("Value is not numeric");
            ingredients.push(ingredient)
        }
    }

    let result = ParsedInput {
        ranges: ranges,
        ingredients: ingredients
    };

    return result;
}

fn main() {
    // Example input
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_input_list: Vec<&str> = example_input.trim().split('\n').collect();
    let parsed_example_input = preprocess_input(&example_input_list);

    // Input
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_list: Vec<&str> = input.trim().split('\n').collect();
    let parsed_input = preprocess_input(&input_list);

    // Part 1 Example
    let part1_example_result = part1(&parsed_example_input);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&parsed_input);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&parsed_example_input);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&parsed_input);
    println!("Part 2: {}", part2_result);
}