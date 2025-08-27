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

import math

def traverse_firewall(firewall_map):
    layers = firewall_map.split("\n")
    result = 0

    for layer in layers:
        (idx, depth) = parse_layer(layer)
        if depth and depth > 0:
            caught = is_scanner_in_pos_0(idx, depth)
            if caught:
                result += idx * depth
    return result

def parse_layer(layer):
    layer_parts = layer.split(":")
    idx = int(layer_parts[0].strip())
    depth = int(layer_parts[1].strip())
    return (idx, depth)

def is_scanner_in_pos_0(time, depth):
    period = (depth - 1) * 2
    return time % period == 0

def run_tests():
    assert(traverse_firewall(part1_test1) == 24)
    assert(traverse_firewall(firewall_map) == 2508)

# print(traverse_firewall(firewall_map))
run_tests()