use std::fs;

// Generalized Part 2 from Python solution to handle both parts
fn part2(battery_banks: &Vec<&str>, num_digits: u32) -> i64 {
    let mut result: i64 = 0;

    for battery_bank in battery_banks {
        let mut bank_value: i64 = 0;
        let mut digits_remaining: u32 = num_digits;
        let mut window_start = 0;

        // Build bank_value one digit at a time
        // Use a sliding window to specify a search window for the next digit
        while digits_remaining > 0 {
            let mut max_significant_digit: i64 = 0;
            digits_remaining -= 1;

            // Sliding window starts on the index after the last digit we found
            // It ends at (length of banks) - (digits remaining)
            // e.g if bank is 987654321 and we still need 6 digits, the search area is 9876
            let window_end = battery_bank.len() - (digits_remaining as usize);
            for idx in window_start..window_end {
                let digit: &i64 = &battery_bank[idx..idx+1].parse().expect("Digit is not numeric");
                if *digit > max_significant_digit {
                    max_significant_digit = *digit;
                    window_start = idx + 1;
                }
            }

            bank_value += max_significant_digit * 10_i64.pow(digits_remaining);
        }

        result += bank_value;
    }

    return result;
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_battery_banks: Vec<&str> = example_input.trim().split('\n').collect();
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let battery_banks: Vec<&str> = input.trim().split('\n').collect();

    // Part 1 Example
    let part1_example_result = part2(&example_battery_banks, 2);
    println!("Part 1 (example): {}", part1_example_result);

    // # Part 1
    let part1_result = part2(&battery_banks, 2);
    println!("Part 1: {}", part1_result);

    // Part 2 Example
    let part2_example_result = part2(&example_battery_banks, 12);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&battery_banks, 12);
    println!("Part 2: {}", part2_result);
}