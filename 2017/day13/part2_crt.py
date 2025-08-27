from math import gcd

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

def parse_layer(layer):
    layer_parts = layer.split(":")
    idx = int(layer_parts[0].strip())
    depth = int(layer_parts[1].strip())
    return (idx, depth)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a, m):
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        return None
    return (x % m + m) % m

def chinese_remainder_theorem(equations):
    if not equations:
        return 0
    
    remainder, modulus = equations[0]
    
    for i in range(1, len(equations)):
        r2, m2 = equations[i]
        
        gcd_val = gcd(modulus, m2)
        
        if (r2 - remainder) % gcd_val != 0:
            return None
        
        a = modulus // gcd_val
        b = m2 // gcd_val
        c = (r2 - remainder) // gcd_val
        
        inv = mod_inverse(a, b)
        if inv is None:
            return None
        
        k1 = (c * inv) % b
        
        remainder = remainder + k1 * modulus
        modulus = (modulus * m2) // gcd_val
        remainder = remainder % modulus
    
    return remainder

def part2_crt(firewall_map):
    layer_lines = firewall_map.split("\n")
    layers = []
    
    for layer in layer_lines:
        idx, depth = parse_layer(layer)
        if depth > 0:
            period = 2 * (depth - 1)
            layers.append((idx, period))
    
    if not layers:
        return 0
    
    def check_delay(delay):
        for idx, period in layers:
            if (delay + idx) % period == 0:
                return False
        return True
    
    lcm = 1
    for _, period in layers:
        lcm = (lcm * period) // gcd(lcm, period)
    
    for delay in range(lcm):
        if check_delay(delay):
            return delay
    
    return None

print(part2_crt(firewall_map))