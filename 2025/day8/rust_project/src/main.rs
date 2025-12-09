use std::fs;
use std::collections::{HashMap, BinaryHeap, HashSet, VecDeque};
use std::cmp;
use std::cmp::Reverse;
use ahash::{HashSetExt, HashMapExt, RandomState};

type Triple = (usize, usize, usize);
type FastHashMap<K, V> = HashMap<K, V, RandomState>;
type FastHashSet<T> = HashSet<T, RandomState>;

struct SimulationResult {
    part1_result: usize,
    part2_result: usize
}

#[derive(Debug, Eq, PartialEq, Ord, PartialOrd)]
struct BoxDistance {
    distance: Reverse<usize>,
    box1_coordinates: Triple,
    box2_coordinates: Triple
}

fn part1(input: &Vec<&str>, num_connections: usize) -> SimulationResult {
    let mut distances: BinaryHeap<BoxDistance> = BinaryHeap::new();
    let mut unique_distances: FastHashSet<(Triple, Triple)> = FastHashSet::new();
    const NUM_CLOSEST_TO_KEEP: usize = 6;

    // Compute distance between boxes. Only keep top K neighbors for each box
    for line1 in input {
        let box1_coordinates = parse_box(line1);
        let mut closest_neighbors: BinaryHeap<BoxDistance> = BinaryHeap::new();

        // Compute all neighbor distances
        for line2 in input {
            let box2_coordinates = parse_box(line2);
            if box1_coordinates != box2_coordinates {
                let distance: usize = get_distance(box1_coordinates, box2_coordinates);
                let box_distance: BoxDistance = BoxDistance {
                    distance: Reverse(distance), // Rust heaps are max by default. Reverse values to make min heap
                    box1_coordinates: box1_coordinates,
                    box2_coordinates: box2_coordinates
                };
                closest_neighbors.push(box_distance);
            }
        }

        // Filter down to closest K
        for _ in 0..NUM_CLOSEST_TO_KEEP {
            let box_distance: BoxDistance = closest_neighbors.pop().expect("No more neighbors!");
            let min_coordinates: Triple = cmp::min(box_distance.box1_coordinates, box_distance.box2_coordinates);
            let max_coordinates: Triple = cmp::max(box_distance.box1_coordinates, box_distance.box2_coordinates);
            let box_tuple: (Triple, Triple) = (min_coordinates, max_coordinates);
            if !unique_distances.contains(&box_tuple) {
                unique_distances.insert(box_tuple);
                distances.push(box_distance);
            }
        }
    }

    // Build a graph of box connections as we make them
    let mut box_adjacencies: FastHashMap<Triple, FastHashSet<Triple>> = FastHashMap::new();
    let mut connections_made: usize = 0;
    let mut part1_result: usize = 0;
    let mut part2_result: usize = 0;

    let mut part2_seen_boxes: FastHashSet<Triple> = FastHashSet::new();
    while distances.len() > 0 {
        let box_distance: BoxDistance = distances.pop().expect("No more distances!");

        // Connect box 1 and box 2
        box_adjacencies
            .entry(box_distance.box1_coordinates)
            .or_insert(FastHashSet::new())
            .insert(box_distance.box2_coordinates);
        box_adjacencies
            .entry(box_distance.box2_coordinates)
            .or_insert(FastHashSet::new())
            .insert(box_distance.box1_coordinates);

        // Part 2, traverse box1's circuit and see if its size is the whole input
        part2_seen_boxes.clear();
        let part2_circuit_size: usize = traverse_circuit(&box_distance.box1_coordinates, &box_adjacencies, &mut part2_seen_boxes);
        if part2_circuit_size == input.len() {
            part2_result = box_distance.box1_coordinates.0 * box_distance.box2_coordinates.0;
            return SimulationResult {
                part1_result: part1_result,
                part2_result: part2_result
            };
        }

        // Part 1, traverse circuits and get their size
        if connections_made == num_connections - 1 {
            let mut seen_boxes: FastHashSet<Triple> = FastHashSet::new();
            let mut biggest_circuits: BinaryHeap<usize> = BinaryHeap::new();
            for box_coordinates in box_adjacencies.keys() {
                if !seen_boxes.contains(box_coordinates) {
                    let circuit_size: usize = traverse_circuit(box_coordinates, &box_adjacencies, &mut seen_boxes);
                    biggest_circuits.push(circuit_size);  
                }
            }

            part1_result = 1;
            for _ in 0..3 {
                part1_result *= biggest_circuits.pop().expect("Not enough circuits");
            }
        }

        connections_made += 1;
    }

    return SimulationResult {
        part1_result: part1_result,
        part2_result: part2_result
    };
}

fn traverse_circuit(box_coordinates: &Triple, box_adjacencies: &FastHashMap<Triple, FastHashSet<Triple>>, seen_boxes: &mut FastHashSet<Triple>) -> usize {
    let mut queue: VecDeque<Triple> = VecDeque::from([*box_coordinates]);
    let mut circuit_size: usize = 0;

    while let Some(current_box) = queue.pop_front() {
        if seen_boxes.insert(current_box) {
            circuit_size += 1;

            if let Some(neighbors) = box_adjacencies.get(&current_box) {
                for neighbor in neighbors {
                    if !seen_boxes.contains(&neighbor) {
                        queue.push_back(*neighbor);
                    }
                }
            }
        }
    }

    return circuit_size;
}

fn parse_box(line: &str) -> Triple {
    let mut parts = line
        .split(',')
        .map(|val| val.parse().expect("Value is not numeric"));
    
    // ⚡ FIX: Direct iterator consumption—NO HEAP ALLOCATION
    let x = parts.next().unwrap_or(0);
    let y = parts.next().unwrap_or(0);
    let z = parts.next().unwrap_or(0);

    (x, y, z)
}

fn get_distance(box1_coordinates: Triple, box2_coordinates: Triple) -> usize {
    let x_distance = box2_coordinates.0.abs_diff(box1_coordinates.0).pow(2);
    let y_distance = box2_coordinates.1.abs_diff(box1_coordinates.1).pow(2);
    let z_distance = box2_coordinates.2.abs_diff(box1_coordinates.2).pow(2);
    return x_distance + y_distance + z_distance;
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
    let example_result: SimulationResult = part1(&example_input_list, 10);
    println!("Part 1 (example): {}", example_result.part1_result);
    println!("Part 2 (example): {}", example_result.part2_result);

    // Part 1 & 2
    let result: SimulationResult = part1(&input_list, 1000);
    println!("Part 1: {}", result.part1_result);
    println!("Part 2: {}", result.part2_result);
}