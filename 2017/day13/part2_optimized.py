part1_test1 = """0: 3
1: 2
4: 4
6: 4"""

firewall_map = """0: 3
1: 2
2: 5
4: 4
6: 4
8: 6
10: 6
12: 6
14: 8
16: 6
18: 8
20: 8
22: 8
24: 12
26: 8
28: 12
30: 8
32: 12
34: 12
36: 14
38: 10
40: 12
42: 14
44: 10
46: 14
48: 12
50: 14
52: 12
54: 9
56: 14
58: 12
60: 12
64: 14
66: 12
70: 14
76: 20
78: 17
80: 14
84: 14
86: 14
88: 18
90: 20
92: 14
98: 18"""


from collections import defaultdict
from math import gcd

# Parse firewall data: d is {depth: range}
d = eval("{"+firewall_map.strip().replace('\n',',')+"}")

# Build constraints: neq[period] contains forbidden residues (mod period)
# For each scanner at depth with range r, it has period = 2*(r-1)
# We need delay != -depth (mod period) to avoid being caught
forbidden_residues = defaultdict(list)
for depth in d.keys():
	period = 2 * (d[depth] - 1)	
	forbidden_residues[period].append((-depth)%(period))
moduli = sorted(forbidden_residues.keys())

# Use Chinese Remainder Theorem to find valid delays
prev_lcm = 1
lcm = 1
possible_delays = [0]  # Start with residue 0 (mod 1)
for modulus in moduli:
	g = gcd(modulus, lcm)  # Greatest common divisor
	prev_lcm = lcm
	lcm = lcm * modulus // g  # New LCM (least common multiple)
	
	# Extend previous residues to new modulus
	extended_delays = []
	for delay in possible_delays:
		for i in range(int(delay), int(lcm), int(prev_lcm)):
			extended_delays.append(i)
	
	# Filter out residues that violate current constraints
	valid_delays = []
	for delay in extended_delays:
		if delay % modulus not in forbidden_residues[modulus]:
			valid_delays.append(delay)
	possible_delays = valid_delays

print(sorted(possible_delays)[0], "(mod", lcm, ")")  # Smallest valid delay