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


def attempt_traversal(layers, delay=0):
    for (idx, depth) in layers:
        if depth and depth > 0:
            caught = is_scanner_in_pos_0(idx, depth, delay)
            if caught:
                return True
            
    return False

def is_scanner_in_pos_0(time, depth, delay):
    period = 2 * (depth - 1)
    return (time + delay) % period == 0

def parse_layer(layer):
    layer_parts = layer.split(":")
    idx = int(layer_parts[0].strip())
    depth = int(layer_parts[1].strip())
    return (idx, depth)

def part2(firewall_map):
    delay = 0
    layer_lines = firewall_map.split("\n")
    layers = []

    for layer in layer_lines:
        layers.append(parse_layer(layer))

    while True:
        was_caught = attempt_traversal(layers, delay)
        if not was_caught:
            return delay

        delay += 1

def run_tests():
    assert(part2(part1_test1) == 10)
    assert(part2(firewall_map) == 3913186)

def part2_better(firewall_map):
    layer_lines = firewall_map.split("\n")
    periods = []
    
    # Calculate the scanner's period for each layer FIRST
    for layer in layer_lines:
        idx, depth = parse_layer(layer)
        if depth > 0:
            periods.append((idx, 2 * (depth - 1)))
 
    # Now try delays until we get through successfully
    delay = 0
    while True:
        caught = False
        for idx, period in periods:
            if period > 0 and (delay + idx) % period == 0:
                caught = True
                break
        
        if not caught:
            return delay
        
        delay += 1


# print(part2(firewall_map))
print(part2_better(firewall_map))

# run_tests()