import sys
from math import gcd # Standard library function to compute the greatest common divisor

# --- Helper Functions ---

def get_divisors(n):
    """
    Finds all proper divisors of n (divisors excluding n itself).
    Returns a sorted list of divisors.
    """
    divs = []
    i = 1
    # Iterate up to the square root of n
    while i * i <= n:
        if n % i == 0:
            # i is a divisor
            if i < n: # Only include proper divisors
                divs.append(i)

            # Check the complementary divisor n // i
            # It should be different from i (for non-perfect squares)
            # and less than n (i.e., not the number itself)
            if i != n // i and n // i < n:
                divs.append(n // i)
        i += 1
    return sorted(divs)


def first_periodic_geq(lo, num_digits, k):
    """
    Finds the smallest number >= lo that has 'num_digits' digits
    and is 'k'-periodic.
    A number is 'k'-periodic if it is formed by repeating its first 'k' digits.
    Example: if num_digits=8 and k=4, 12341234 is 4-periodic.
    """
    reps = num_digits // k # Number of times the prefix of length k is repeated
    # The smallest k-digit number and the largest k-digit number
    min_prefix, max_prefix = 10 ** (k - 1), 10 ** k - 1
    
    # Get the prefix of length k from lo (padded with zeros if needed)
    lo_prefix_str = str(lo).zfill(num_digits)[:k]
    lo_prefix = int(lo_prefix_str)

    # 1. Test the candidate formed by repeating lo_prefix
    candidate = int(lo_prefix_str * reps)
    
    if candidate >= lo:
        # Candidate is within the range [lo, ...]
        if lo_prefix >= min_prefix:
            # The prefix itself is a valid k-digit number (not starting with 0, unless k=1)
            return candidate
        else:
            # lo_prefix was a prefix of a number with fewer than k digits,
            # so the minimum valid k-digit prefix is min_prefix
            return int(str(min_prefix) * reps)

    # 2. Candidate is too small (< lo), try the next prefix
    lo_prefix += 1
    
    if lo_prefix > max_prefix:
        # If the next prefix exceeds the maximum k-digit number, no such periodic number exists
        return None
        
    # Construct and return the number with the incremented prefix
    return int(str(max(lo_prefix, min_prefix)) * reps)


def last_periodic_leq(hi, num_digits, k):
    """
    Finds the largest number <= hi that has 'num_digits' digits
    and is 'k'-periodic.
    """
    reps = num_digits // k # Number of times the prefix is repeated
    # The smallest k-digit number and the largest k-digit number
    min_prefix, max_prefix = 10 ** (k - 1), 10 ** k - 1
    
    # Get the prefix of length k from hi (padded with zeros if needed)
    hi_prefix_str = str(hi).zfill(num_digits)[:k]
    hi_prefix = int(hi_prefix_str)

    # 1. Test the candidate formed by repeating hi_prefix
    candidate = int(hi_prefix_str * reps)
    
    if candidate <= hi:
        # Candidate is within the range [..., hi]
        if min_prefix <= hi_prefix <= max_prefix:
            # The prefix is a valid k-digit number
            return candidate
        # If hi_prefix > max_prefix, it means hi has more than num_digits, 
        # but the function expects hi to have 'num_digits'. This is a safety/boundary check.
        # If hi_prefix is too large, use the largest possible prefix
        return int(str(max_prefix) * reps) if hi_prefix > max_prefix else None

    # 2. Candidate is too large (> hi), try the previous prefix
    hi_prefix -= 1
    
    # If the previous prefix is less than the minimum k-digit number, 
    # no such periodic number exists in the desired digit count
    return None if hi_prefix < min_prefix else int(str(hi_prefix) * reps)


def count_periodic_in_range(lo, hi, num_digits, k):
    """
    Counts and sums all k-periodic numbers in the range [lo, hi]
    that have exactly 'num_digits' digits.
    Returns: (count, sum)
    """
    # Find the first valid k-periodic number >= lo
    first = first_periodic_geq(lo, num_digits, k)
    if first is None or first > hi:
        return 0, 0

    # Find the last valid k-periodic number <= hi
    last = last_periodic_leq(hi, num_digits, k)
    if last is None or last < lo or first > last:
        return 0, 0

    reps = num_digits // k
    # The set of k-periodic numbers is determined by their k-digit prefix
    first_prefix, last_prefix = int(str(first)[:k]), int(str(last)[:k])
    
    # The number of periodic numbers is simply the count of possible prefixes
    count = last_prefix - first_prefix + 1

    # All k-periodic numbers P with prefix p can be written as P = p * multiplier
    # where multiplier = (10^(r*k) - 1) / (10^k - 1), r = reps.
    # E.g., for k=2, reps=2 (4 digits), prefix=12, number=1212.
    # 1212 = 12 * 101. Multiplier = (10^4 - 1) / (10^2 - 1) = 9999 / 99 = 101.
    multiplier = (10 ** (reps * k) - 1) // (10 ** k - 1)
    
    # The sum of all prefixes (arithmetic progression sum)
    prefix_sum = (first_prefix + last_prefix) * count // 2
    
    # The total sum is the sum of prefixes multiplied by the constant multiplier
    return count, prefix_sum * multiplier


# --- Main Logic Functions ---

def sum_invalid_in_fixed_digit_range(lo, hi, num_digits):
    """
    Calculates the sum of all numbers N in [lo, hi] (all having 'num_digits')
    such that N is 'k'-periodic for some PROPER divisor k of 'num_digits'.
    
    This uses the Inclusion-Exclusion Principle (or more accurately, a modified
    version based on minimal periodicity).
    """
    # Get all proper divisors of num_digits (k < num_digits)
    divs = get_divisors(num_digits)
    if not divs:
        # If num_digits is prime (or 1), the only proper divisor is 1.
        # But get_divisors(n) only returns proper divisors. If n=1, it's 0. 
        # If n > 1 and prime, only proper divisor is 1, which is always in range.
        # It's an edge case check.
        return 0 

    # 1. Calculate the count and sum of all k-periodic numbers for each k in divs
    periodic = {k: count_periodic_in_range(lo, hi, num_digits, k) for k in divs}
    
    # 2. Calculate the count and sum of numbers with MINIMAL periodicity k
    # A number with minimal k-periodicity is NOT q-periodic for any q that 
    # is a proper divisor of k.
    minimal_cnt, minimal_sum = {}, {}

    for k in divs:
        cnt, s = periodic[k]
        # Subtract counts/sums of numbers whose minimal period q PROPERLY divides k.
        # These are already accounted for by minimal_cnt[q] and minimal_sum[q].
        for q in divs:
            if q < k and k % q == 0:
                cnt -= minimal_cnt[q]
                s -= minimal_sum[q]
        # Store the count/sum for numbers with minimal k-periodicity
        minimal_cnt[k], minimal_sum[k] = cnt, s
    
    # The total sum of all periodic numbers is the sum of the sums of numbers
    # grouped by their minimal period.
    return sum(minimal_sum.values())


def split_range_by_digits(lo, hi):
    """
    Splits a large range [lo, hi] into sub-ranges where all numbers 
    in a sub-range have the same number of digits.
    
    Returns: list of (sub_lo, sub_hi, num_digits)
    Example: [1, 100] -> [(1, 9, 1), (10, 99, 2), (100, 100, 3)]
    """
    ranges = []
    current = lo
    while current <= hi:
        num_digits = len(str(current))
        # The end of the sub-range is either 'hi' or the largest number with 'num_digits'
        range_end = min(hi, 10 ** num_digits - 1)
        ranges.append((current, range_end, num_digits))
        current = range_end + 1
    return ranges


def solve(input_str):
    """
    Main function to parse the input and calculate the total sum.
    The input is a string of comma-separated ranges, e.g., "1-100, 500-600".
    
    The problem being solved is likely:
    Calculate the sum of all numbers N in the input ranges that have a
    k-periodic structure, where k is a proper divisor of the number of digits of N.
    """
    ranges = []
    # Parse the input string into a list of (lo, hi) tuples
    for part in input_str.strip().rstrip(',').split(','):
        if '-' in part:
            a, b = part.strip().split('-')
            ranges.append((int(a), int(b)))

    # Iterate over the input ranges, split them by digit count, and sum the results
    return sum(
        sum_invalid_in_fixed_digit_range(sub_lo, sub_hi, d)
        for lo, hi in ranges # For each user-defined range [lo, hi]
        for sub_lo, sub_hi, d in split_range_by_digits(lo, hi) # For each sub-range with a fixed digit count 'd'
    )


if __name__ == "__main__":
    # --- Execution Block ---
    if len(sys.argv) < 2:
        print("Usage: python solution_optimized.py <input_file>")
        sys.exit(1)

    # Read the input from the specified file (sys.argv[1])
    with open(sys.argv[1]) as f:
        print(solve(f.read()))