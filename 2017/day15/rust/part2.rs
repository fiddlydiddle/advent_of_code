const GEN_A_SEED: u64 = 634;
const GEN_A_FACTOR: u64 = 16807;
const GEN_A_MODULUS: u64 = 4;
const GEN_B_SEED: u64 = 301;
const GEN_B_FACTOR: u64 = 48271;
const GEN_B_MODULUS: u64 = 8;
const DIVISOR: u64 = 2147483647;
const MAX_PAIRS: u64 = 5000000;

fn count_matches(mut gen_a_val: u64, mut gen_b_val: u64) {
    let mut num_matches = 0;
    for _ in 0..MAX_PAIRS {
        gen_a_val = get_next_val(gen_a_val, GEN_A_FACTOR, GEN_A_MODULUS);
        gen_b_val = get_next_val(gen_b_val, GEN_B_FACTOR, GEN_B_MODULUS);
    
        if (gen_a_val as u16) == (gen_b_val as u16) {
            num_matches += 1;
        }
    }

    println!("{}", num_matches)
}

fn get_next_val(current_val: u64, factor: u64, modulus: u64) -> u64 {
    let mut new_val = current_val * factor % DIVISOR;
    while new_val % modulus != 0 {
        new_val = (new_val * factor) % DIVISOR
    }
    return new_val;
}

fn main() {
    count_matches(GEN_A_SEED, GEN_B_SEED);
}