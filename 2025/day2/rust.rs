use std::fs;

fn part1(ranges: &Vec<&str>) -> i64 {
    let mut invalid_ids: Vec<i64> = Vec::new();

    for range in ranges {
        let range_parts: Vec<&str> = range.split('-').collect();
        let start_val: i64 = range_parts[0].parse().expect("Range part is not numeric");
        let end_val: i64 = range_parts[1].parse().expect("Range part is not numeric");

        for val_to_check in start_val..end_val + 1 {
            let val_length = val_to_check.to_string().len();
            // Take substrings of size j // 2 and see if they are repeated 
            if val_length % 2 == 0 {
                let substring = &val_to_check.to_string()[0..val_length/2];
                if substring.repeat(2) == val_to_check.to_string() {
                    invalid_ids.push(val_to_check);
                }
            }
        }
    }

    return invalid_ids.iter().sum();
}

fn part2(ranges: &Vec<&str>) -> i64 {
    let mut invalid_ids: Vec<i64> = Vec::new();

    for range in ranges {
        let range_parts: Vec<&str> = range.split('-').collect();
        let start_val: i64 = range_parts[0].parse().expect("Range part is not numeric");
        let end_val: i64 = range_parts[1].parse().expect("Range part is not numeric");

        for val_to_check in start_val..end_val + 1 {
            let val_length = val_to_check.to_string().len();

            // Take substrings of size i and see if they are repeated 
            for i in 1..val_length {
                if val_length % i == 0 {
                    let substring = &val_to_check.to_string()[0..i];
                    let num_repititions = val_length / i;
                    if substring.repeat(num_repititions) == val_to_check.to_string() {
                        invalid_ids.push(val_to_check);
                        break;
                    }
                }
            }
        }
    }

    return invalid_ids.iter().sum();
}


fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_ranges: Vec<&str> = example_input.trim().split(',').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let ranges: Vec<&str> = input.trim().split(',').collect();

    // Part 1 Example
    let part1_example_result = part1(&example_ranges);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part1(&ranges);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_ranges);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&ranges);
    println!("Part 2: {}", part2_result);
}