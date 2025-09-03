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

# d is {depth:range}, eg:
d = eval("{"+firewall_map.strip().replace('\n',',')+"}")

neq = defaultdict(list) # of the form {b:[a1,a2...]} where delay != a_i (mod b)
for depth in d.keys():
	neq[d[depth]*2-2] +=  [(-depth)%(d[depth]*2-2)]
moduli = sorted(neq.keys())

prev_lcm=1
lcm = 1
residues = [0] #mod 1
for m in moduli:
	g = gcd(m,lcm) # simple Euclidean algorithm
	prev_lcm = lcm
	lcm = lcm*m//g  #new modulus
	residues = [x for x in
		sum([list(range(int(i),int(lcm),int(prev_lcm))) for i in residues],[])
		if x%m not in neq[m]]

print(sorted(residues)[0], "(mod",lcm,")") # the smallest residue