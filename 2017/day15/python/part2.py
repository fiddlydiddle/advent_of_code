GEN_A_SEED = 634
GEN_B_SEED = 301
BITMASK = 65535 # For comparing last 16 digits of binary number

def count_matches(gen_a_val, gen_b_val):
    num_matches = 0

    for _ in range(5000000):

        gen_a_val = get_next_val(gen_a_val, 16807, 4)
        gen_b_val = get_next_val(gen_b_val, 48271, 8)

        # Use bitwise operation to compare last 16 bits
        if (gen_a_val & BITMASK) == (gen_b_val & BITMASK):
            num_matches += 1

    print(num_matches)

def get_next_val(current_val, factor, modulus):
    new_val = current_val * factor % 2147483647
    while new_val % modulus != 0:
        new_val = new_val * factor % 2147483647

    return new_val


count_matches(GEN_A_SEED, GEN_B_SEED)