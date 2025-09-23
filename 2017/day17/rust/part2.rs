fn main() {
    println!("{}", part1(3, 2017)); // Correct answer: 638
    println!("{}", part1(304, 2017)); // Correct answer: 1173
    println!("{}", part2(304, 50_000_000)); // Correct answer: 1930815
}

fn part1(steps_per_iteration: u64, num_iterations: u64) -> u64 {
    let mut buffer = vec![0];
    let mut current_position = 0;

    for val_to_insert in 1..=num_iterations {
        current_position = (current_position + steps_per_iteration) % (buffer.len() as u64);
        buffer.insert((current_position + 1) as usize, val_to_insert);
        current_position += 1;
    }
    
    return buffer[((current_position + 1) as usize) % buffer.len()]
}

fn part2(steps_per_iteration: u64, num_iterations: u64) -> u64 {
    let mut current_position = 0;
    let mut result = 0;
    for val_to_insert in 1..=num_iterations {
        current_position = (current_position + steps_per_iteration) % val_to_insert;
        if current_position == 0 {
            result = val_to_insert;
        }
        current_position += 1;
    }

    return result;
}