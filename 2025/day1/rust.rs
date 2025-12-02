use std::fs;

fn part1(input: &Vec<&str>) -> i32 {
    let mut current_val: i32 = 50;
    let mut result: i32 = 0;

    for line in input {
        // Parse line for direction and steps
        let direction = line.chars().next().unwrap();
        let sign: i32 = if direction == 'R' {
            1
        } else {
            -1
        };
        let steps: &i32 = &line[1..].parse().expect("The given slice is not numeric");

        // Perform steps in direction
        current_val += steps * sign;

        // Take modulus to handle dial wrapping
        current_val %= 100;

        // Increment result if we land on 0
        if current_val == 0 {
            result += 1;
        }
    }

    return result;
}

fn part2(input: &Vec<&str>) -> i32 {
    let mut current_val: i32 = 50;
    let mut result: i32 = 0;

    for line in input {
        // Parse line for direction and steps
        let direction = line.chars().next().unwrap();
        let sign: i32 = if direction == 'R' {
            1
        } else {
            -1
        };
        let steps: i32 = line[1..].parse().expect("The given slice is not numeric");

        for _ in 0..steps {
            // Perform a step in direction
            current_val += sign;

            // Take modulus to handle dial wrapping
            current_val %= 100;

            // Increment result if we land on 0
            if current_val == 0 {
                result += 1;
            }
        }
    }
    return result;
}

fn part2_optimized(input: &Vec<&str>) -> i32 {
    let mut current_val: i32 = 50;
    let mut result: i32 = 0;

    for line in input {
        // Parse line for direction and steps
        let direction = line.chars().next().unwrap();
        let sign: i32 = if direction == 'R' {
            1
        } else {
            -1
        };
        let steps: i32 = line[1..].parse().expect("The given slice is not numeric");
        
        let change: i32 = steps * sign;
        
        let old_position = current_val;
        let new_position = old_position + change;
        
        if change > 0 {
            // Take floor of new_position divided by 100. Same for old_position.
            // Num zeroes is the difference between the two.
            let old_loops = old_position / 100;
            let new_loops = new_position / 100;
            result += new_loops - old_loops;
        }
        else if change <= 0 {
            // Take ceiling of new_position divided by 100. Same for old_position
            // Num zeros is the defference between the two.
            let old_loops: i32 = (((old_position as f64) / 100.0).ceil() - 1.0) as i32;
            let new_loops: i32 = (((new_position as f64) / 100.0).ceil() - 1.0) as i32;
            result += old_loops - new_loops;
        }

        current_val = (new_position % 100 + 100) % 100;
    }
        
    return result;
}


fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_instructions: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let instructions: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_instructions);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&instructions);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_instructions);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&instructions);
    println!("Part 2: {}", part2_result);
}