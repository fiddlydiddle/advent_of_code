gen_a_seed = 634
gen_b_seed = 301

def count_matches(gen_a_seed, gen_b_seed):
    gen_a_factor = 16807
    gen_b_factor = 48271

    gen_a_prev_val = gen_a_seed
    gen_b_prev_val = gen_b_seed

    matches = []

    for i in range(40000000):
        gen_a_new_val = get_next_val(gen_a_prev_val, gen_a_factor)
        gen_b_new_val = get_next_val(gen_b_prev_val, gen_b_factor)

        if bin(gen_a_new_val)[-16::] == bin(gen_b_new_val)[-16::]:
            matches.append(i)

        gen_a_prev_val = gen_a_new_val
        gen_b_prev_val = gen_b_new_val

    print(len(matches))

def get_next_val(current_val, factor):
    return current_val * factor % 2147483647


count_matches(gen_a_seed, gen_b_seed)