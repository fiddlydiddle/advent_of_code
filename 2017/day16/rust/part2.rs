use std::fs;

fn main() {
    part2();
}

fn part2() {
    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");

    let moves: Vec<&str> = input.trim().split(',').collect();
    let mut programs: [char; 16] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'];
    let initial_state = "abcdefghijklmnop";
    let mut cycle_length = 1;

    // Look for cycle in program positions
    loop {
        part1(&mut programs, &moves);
        if programs.iter().collect::<String>() == initial_state {
            break;
        }
        cycle_length += 1;
    }

    // Now we don't need to run the dance a billion times, just 1,000,000,000mod(cycle_length) times
    for i in 0..(1_000_000_000 % cycle_length) {
        part1(&mut programs, &moves);

        if i == 0 {
            println!("{}", programs.iter().collect::<String>());
        }
    }
    
    println!("{}", programs.iter().collect::<String>());
}

fn part1(programs: &mut [char; 16], moves: &Vec<&str>) {
    for &move_str in moves {
        let move_type = move_str.chars().next().unwrap();
        let rest_of_move = &move_str[1..];

        match move_type {
            's' => {
                let spin_num: usize = rest_of_move.parse().expect("Invalid spin number");
                programs.rotate_right(spin_num);
            }
            'x' => {
                let mut coordinates = rest_of_move.split('/');
                let pos1: usize = coordinates.next().unwrap().parse().expect("Invalid position");
                let pos2: usize = coordinates.next().unwrap().parse().expect("Invalid position");
                
                programs.swap(pos1, pos2);
            }
            'p' => {
                let mut coordinates = rest_of_move.split('/');
                let char1 = coordinates.next().unwrap().chars().next().unwrap();
                let char2 = coordinates.next().unwrap().chars().next().unwrap();
                let pos1 = programs.iter().position(|&c| c == char1).expect("Character not found");
                let pos2 = programs.iter().position(|&c| c == char2).expect("Character not found");

                programs.swap(pos1, pos2);
            }
            _ => {
                // Handle unknown move types
                eprintln!("Unknown move type: {}", move_type);
            }
        }
    }
}