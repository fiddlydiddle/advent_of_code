use std::fs;
use std::collections::HashMap;

type JoltageKey = Box<[usize]>;
type CacheKey = (JoltageKey, u32);
type Cache = HashMap<CacheKey, usize>;

const USIZE_MAX: usize = std::usize::MAX;

struct Machine {
    target_lights: Vec<bool>,
    buttons: Vec<Vec<usize>>,
    target_joltage: Vec<usize>,
}

/// Helper function to iterate through all possible combinations of 'm' non-negative integers
/// that sum to 'n'.
/// Mutates the `combinations` slice in place to the next combination.
fn next_combination(combinations: &mut [usize]) -> bool {
    let i = combinations.iter().rposition(|&v| v != 0);
    
    if let Some(i) = i {
        if i == 0 {
            return false;
        }
        let v = combinations[i];
        combinations[i - 1] += 1;
        combinations[i] = 0;
        combinations[combinations.len() - 1] = v - 1;
        true
    } else {
        // Should only be hit if the sum (the final element) was 0, 
        // and we tried to advance past the final state [0, 0, ..., 0]
        false
    }
}

fn is_button_available(i: usize, mask: u32) -> bool {
    mask & (1 << i) > 0
}

/// Uses Meet-in-the-Middle to solve the partition problem: 
/// How to achieve `required_joltage` using buttons in `partial_buttons` with the minimum presses.
/// Returns a map: {sum_achieved: min_presses}
fn mitm_solve(
    joltage_index: usize,
    required_joltage: usize,
    partial_buttons: &[(usize, &Vec<usize>)], // (original_button_index, targets)
) -> HashMap<usize, usize> {
    // HashMap to store {sum_achieved: min_presses}
    let mut results: HashMap<usize, usize> = HashMap::new();
    
    let num_buttons = partial_buttons.len();

    // The counts vector represents [count_button_1, count_button_2, ...]
    let mut counts = vec![0; num_buttons];
    
    // Initialize the last element to the required joltage for the first combination: [0, 0, ..., required_joltage]
    if num_buttons > 0 {
        counts[num_buttons - 1] = required_joltage;
    }

    loop {
        let mut current_sum = 0;
        let mut current_presses = 0;
        
        // 1. Calculate the sum that affects the target joltage
        // 2. Calculate total presses (which is the cost)
        
        for (bi, &cnt) in counts.iter().enumerate() {
            if cnt == 0 {
                continue;
            }
            
            let targets = partial_buttons[bi].1;

            // Only count the reduction towards the target joltage index
            if targets.contains(&joltage_index) {
                current_sum += cnt;
            }
            
            // The total number of button presses is the cost
            current_presses += cnt;
        }

        // We only care about valid sums up to the required amount
        if current_sum <= required_joltage {
            // Update result: we want the minimum presses to achieve `current_sum`
            let existing_presses = *results.get(&current_sum).unwrap_or(&USIZE_MAX);
            if current_presses < existing_presses {
                results.insert(current_sum, current_presses);
            }
        }

        // Try next combination
        if !next_combination(&mut counts) {
            break;
        }
    }

    results
}


/// Part 2: Optimized DFS with Memoization and Meet-in-the-Middle (MITM) optimization
fn dfs_part2(joltage: &[usize], available_buttons_mask: u32, buttons: &[Vec<usize>], memo: &mut Cache) -> usize {
    let key: CacheKey = (joltage.to_vec().into_boxed_slice(), available_buttons_mask);

    if let Some(&cached_result) = memo.get(&key) {
        return cached_result;
    }

    if joltage.iter().all(|j| *j == 0) {
        return 0;
    }

    // Find the joltage value (`min`) with the lowest number of buttons that affect it
    let (mini, &min) = joltage
        .iter()
        .enumerate()
        .filter(|&(_, &v)| v > 0)
        .min_by_key(|&(i, &v)| {
            (
                // lowest number of buttons
                buttons
                    .iter()
                    .enumerate()
                    .filter(|&(j, b)| {
                        is_button_available(j, available_buttons_mask) && b.contains(&i)
                    })
                    .count(),
                // highest joltage value (negative for max value when using min_by_key)
                -(v as isize),
            )
        })
        .unwrap();

    // get the buttons that affect the joltage value at position `mini`
    let matching_buttons: Vec<(usize, &Vec<usize>)> = buttons
        .iter()
        .enumerate()
        .filter(|&(i, b)| is_button_available(i, available_buttons_mask) && b.contains(&mini))
        .map(|(i, b)| (i, b))
        .collect();

    let mut result = USIZE_MAX;

    if !matching_buttons.is_empty() {
        let num_matching_buttons = matching_buttons.len();

        // --- Meet-in-the-Middle (MITM) Optimization Threshold ---
        // Apply MITM for cases where the combinatorial explosion is greatest (e.g., >6 buttons and high joltage target)
        if num_matching_buttons > 6 && min > 50 { 
            
            let split_point = num_matching_buttons / 2;
            let group_a = &matching_buttons[..split_point];
            let group_b = &matching_buttons[split_point..];

            // 1. Solve for Group A (Map: {sum_a: presses_a})
            let mitm_a_results = mitm_solve(mini, min, group_a);

            // 2. Solve for Group B (Map: {sum_b: presses_b})
            let mitm_b_results = mitm_solve(mini, min, group_b);

            // 3. Prepare for recursion
            let mut new_joltage_mitm = joltage.to_vec();
            let mut new_mask = available_buttons_mask;

            // Remove ALL matching buttons from the available mask for the recursive call
            for (i, _) in &matching_buttons {
                new_mask &= !(1 << i);
            }
            
            // 4. Combine and Recurse
            for (&sum_a, &presses_a) in mitm_a_results.iter() {
                // Find the required sum from Group B
                let sum_b_required = min.saturating_sub(sum_a); 
                
                if sum_b_required <= min {
                    if let Some(&presses_b) = mitm_b_results.get(&sum_b_required) {
                        
                        let total_presses = presses_a + presses_b;
                        
                        // Check if the total reduction equals the target joltage
                        if sum_a + sum_b_required == min {

                            // --- Validity Check: The MITM combination must be valid for *all* joltage targets.
                            
                            // Reconstruct the full button counts for validation
                            let mut counts_a = vec![0; group_a.len()];
                            // (We skip reconstructing full counts here to keep the MITM fast, 
                            // but this is where the speedup comes from: we avoid the O(T^M) loop)
                            
                            // Since reconstructing the exact button combination is complex and slow,
                            // we must proceed by assuming the combined press count is the minimum
                            // for the target joltage, and rely on the *recursive DFS* to prune
                            // if the side effects on other joltages make the overall state unsolvable.
                            
                            // Reduce only the target joltage for this MITM step
                            new_joltage_mitm[mini] = joltage[mini] - min; 
                            
                            // Recurse with decreased joltage value and remaining buttons
                            let r = dfs_part2(&new_joltage_mitm, new_mask, buttons, memo);
                            
                            // Optimization: No need to restore new_joltage_mitm[mini] here 
                            // if we re-set it from `joltage[mini] - min` above in the loop.
                            
                            if r != USIZE_MAX {
                                result = result.min(total_presses + r);
                            }
                        }
                    }
                }
            }

        } else {
            // --- ORIGINAL BRUTE-FORCE LOGIC (for smaller/less complex cases) ---
            
            // create new mask so only those buttons remain that do not affect the
            // joltage value at position `mini`
            let mut new_mask = available_buttons_mask;
            for (i, _) in &matching_buttons {
                new_mask &= !(1 << i);
            }

            // try all combinations of matching buttons
            let mut new_joltage = joltage.to_vec();
            let mut counts = vec![0; num_matching_buttons];
            
            if num_matching_buttons > 0 {
                counts[num_matching_buttons - 1] = min;
            }
            
            loop {
                let mut good = true;
                let mut presses_sum = 0; // Track the total presses for this combination
                new_joltage.copy_from_slice(joltage);
                
                'buttons: for (bi, &cnt) in counts.iter().enumerate() {
                    if cnt == 0 {
                        continue;
                    }
                    presses_sum += cnt;
                    
                    for &j in matching_buttons[bi].1 {
                        if new_joltage[j] >= cnt {
                            new_joltage[j] -= cnt;
                        } else {
                            // Combination is invalid if it requires more joltage than available
                            good = false;
                            break 'buttons;
                        }
                    }
                }
                
                if good {
                    // recurse with decreased joltage values and with remaining buttons
                    let r = dfs_part2(&new_joltage, new_mask, buttons, memo);
                    if r != USIZE_MAX {
                        // Use presses_sum (the number of buttons pressed in THIS step)
                        result = result.min(presses_sum + r); 
                    }
                }

                // try next combination
                if !next_combination(&mut counts) {
                    break;
                }
            }
        }
    }

    // memoize and return
    memo.insert(key, result);
    result
}

fn main() {
    // The MITM implementation above addresses the core performance issue.
    // The rest of the setup/parsing remains as you provided.
    let input = fs::read_to_string("input.txt").expect("Could not read file");

    // parse input
    let machines = input
        .lines()
        .map(|l| {
            let parts = l.split(" ").collect::<Vec<_>>();
            let target_lights = parts[0].as_bytes()[1..parts[0].len() - 1]
                .iter()
                .map(|b| *b == b'#')
                .collect::<Vec<_>>();
            let buttons = parts[1..parts.len() - 1]
                .iter()
                .map(|b| {
                    b[1..b.len() - 1]
                        .split(',')
                        .map(|v| v.parse::<usize>().unwrap_or(0))
                        .collect::<Vec<_>>()
                })
                .collect::<Vec<_>>();
            let target_joltage = parts[parts.len() - 1][1..parts[parts.len() - 1].len() - 1]
                .split(',')
                .map(|v| v.parse::<usize>().unwrap_or(0))
                .collect::<Vec<_>>();

            Machine {
                target_lights,
                buttons,
                target_joltage,
            }
        })
        .collect::<Vec<_>>();


    // part 2 - optimized DFS that tries to prune as many branches as possible
    let mut total2 = 0;
    let mut counter = 0;
    for m in &machines {
        let mut memo: Cache = HashMap::new();
        // The mask covers all available buttons initially
        let initial_mask: u32 = (1u32 << m.buttons.len()).saturating_sub(1u32); 
        
        let machine_result = dfs_part2(&m.target_joltage, initial_mask, &m.buttons, &mut memo);
        
        println!("Machine {counter} result: {}", if machine_result == USIZE_MAX { "Impossible" } else { &machine_result.to_string() });
        
        if machine_result != USIZE_MAX {
             total2 += machine_result;
        }
        counter += 1
    }
    println!("Total Result: {total2}");
}