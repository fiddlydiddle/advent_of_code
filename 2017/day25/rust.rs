fn part1() -> i32 {
    const TAPE_SIZE: usize = 15_000;
    const CHECKSUM_STEPS: i64 = 12_386_363;

    let mut tape = [0u8; TAPE_SIZE];
    let mut current_state: char = 'a';
    let mut current_idx: usize = TAPE_SIZE / 2;
    let mut checksum_count: i32 = 0;

    for _ in 0..CHECKSUM_STEPS {
        let current_val: u8 = tape[current_idx];

        match current_state {
            'a' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx += 1;
                    current_state = 'b';
                } else {
                    tape[current_idx] = 0;
                    checksum_count -= 1;
                    current_idx -= 1;
                    current_state = 'e';
                }
            }
            'b' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx -= 1;
                    current_state = 'c';
                } else {
                    tape[current_idx] = 0;
                    checksum_count -= 1;
                    current_idx += 1;
                    current_state = 'a';
                }
            }
            'c' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx -= 1;
                    current_state = 'd';
                } else {
                    tape[current_idx] = 0;
                    checksum_count -= 1;
                    current_idx += 1;
                    current_state = 'c';
                }
            }
            'd' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx -= 1;
                    current_state = 'e';
                } else {
                    tape[current_idx] = 0;
                    checksum_count -= 1;
                    current_idx -= 1;
                    current_state = 'f';
                }
            }
            'e' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx -= 1;
                    current_state = 'a';
                } else {
                    current_idx -= 1;
                    current_state = 'c';
                }
            }
            'f' => {
                if current_val == 0 {
                    tape[current_idx] = 1;
                    checksum_count += 1;
                    current_idx -= 1;
                    current_state = 'e';
                } else {
                    current_idx += 1;
                    current_state = 'a';
                }
            }
            _ => panic!("invalid state"),
        }
    }

    checksum_count
}

fn main() {
    let result = part1();
    println!("Part 1: {}", result);
}