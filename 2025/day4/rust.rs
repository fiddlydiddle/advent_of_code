use std::fs;

struct PartOneResult {
    grid: Vec<Vec<bool>>,
    rolls_removed: i32
}

const NEIGHBOR_OFFSETS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
];

fn part1(grid: &Vec<Vec<bool>>, remove_rolls: bool) -> PartOneResult {
    let mut new_grid: Vec<Vec<bool>> = grid.clone();
    let height: i32 = new_grid.len() as i32;
    let width: i32 = new_grid[0].len() as i32;
    let mut rolls_removed: i32 = 0;

    for row_idx in 0..height as usize {
        for col_idx in 0..width as usize {
            let row_idx_i32: i32 = row_idx as i32;
            let col_idx_i32: i32 = col_idx as i32;

            if new_grid[row_idx][col_idx] {
                let mut num_neighbors: i32 = 0;
                for (row_offset, col_offset) in NEIGHBOR_OFFSETS {
                    let neighbor_row_idx: i32 = row_idx_i32 + row_offset;
                    let neighbor_col_idx: i32 = col_idx_i32 + col_offset;
                    if is_inbounds(neighbor_row_idx, neighbor_col_idx, height, width) {
                        if new_grid[neighbor_row_idx as usize][neighbor_col_idx as usize] {
                            num_neighbors += 1;
                        }
                    }
                }

                if num_neighbors < 4 {
                    rolls_removed += 1;
                    if remove_rolls {
                        new_grid[row_idx as usize][col_idx as usize] = false;
                    }
                }
            }
        }
    }

    let result = PartOneResult {
        grid: new_grid,
        rolls_removed: rolls_removed
    };

    return result;
}

fn part2(grid: &Vec<Vec<bool>>) -> i32 {
    let mut new_grid: Vec<Vec<bool>> = grid.clone();
    let mut result: i32 = 0;
    let mut num_rolls_removed: i32 = 1;

    while num_rolls_removed > 0 {
        let part1_result: PartOneResult = part1(&new_grid, true);
        new_grid = part1_result.grid;
        num_rolls_removed = part1_result.rolls_removed;
        result += num_rolls_removed;
    }

    return result;
}

fn is_inbounds(row_idx: i32, col_idx: i32, height: i32, width: i32) -> bool {
    return row_idx >= 0 && row_idx < height && col_idx >= 0 && col_idx < width;
}

fn preprocess_input(input: &Vec<&str>) -> Vec<Vec<bool>> {
    let mut grid: Vec<Vec<bool>> = Vec::new();

    for line in input {
        let mut line_vec: Vec<bool> = Vec::new();
        for char in line.chars() {
            let is_roll: bool = char == '@';
            line_vec.push(is_roll);
        }
        grid.push(line_vec);
    }

    return grid;
}

fn main() {
    let example_input = fs::read_to_string("example.txt")
        .expect("Something went wrong reading the file");
    let example_input_list: Vec<&str> = example_input.trim().split('\n').collect();
    let example_grid = preprocess_input(&example_input_list);

    let input = fs::read_to_string("input.txt")
        .expect("Something went wrong reading the file");
    let input_list: Vec<&str> = input.trim().split('\n').collect();
    let input_grid = preprocess_input(&input_list);

    // Part 1 Example
    let part1_example_result = part1(&example_grid, false);
    println!("Part 1 (example): {}", part1_example_result.rolls_removed);

    // # Part 1
    let part1_result = part1(&input_grid, false);
    println!("Part 1: {}", part1_result.rolls_removed);

    // Part 2 Example
    let part2_example_result = part2(&example_grid);
    println!("Part 2 (example): {}", part2_example_result);

    // Part 2
    let part2_result = part2(&input_grid);
    println!("Part 2: {}", part2_result);
}