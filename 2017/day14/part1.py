def part1():
    input = open('input.txt', 'r').readline()

    used_space = 0
    for i in range(128):
        row_hash = hash_string(f"{input}-{i}")
        for char in row_hash:
            binary_hash = str(bin(int(char, 16))[2:])
            for char in binary_hash:
                if char != "0":
                    used_space += 1
    print(used_space)

def hash_string(string):
    num_list = [i for i in range(256)]
    twists = []
    for character in string:
        ascii_val = ord(character)
        twists.append(ascii_val)

    twists.extend([17, 31, 73, 47, 23])
    current_position = 0
    skip_length = 0

    # Perform the twists 64 times
    for i in range(64):
        (current_position, skip_length) = perform_twists(num_list, twists, current_position, skip_length)

    # Compute dense hash
    dense_hash = []
    for i in range(16):
        hash_item = num_list[i * 16]
        for j in range(1,16):
            hash_item = hash_item ^ num_list[i * 16 + j]
        dense_hash.append(hash_item)

    # Convert each item of densh hash to two digit hex and concat to one string
    return "".join(format(number, "02x") for number in dense_hash)

def perform_twists(num_list, twists, current_position, skip_length):
    for length in twists:
        starting_position = current_position
        ending_position = starting_position + length - 1

        # Perform "twist" by swapping starting and ending characters
        # Take mod(length of list) to handle wrapping
        while starting_position < ending_position:
            
            num_list[starting_position % len(num_list)], num_list[ending_position % len(num_list)] \
                = num_list[ending_position % len(num_list)], num_list[starting_position % len(num_list)]

            starting_position += 1
            ending_position -= 1

        current_position = (current_position + length + skip_length) % len(num_list)
        skip_length += 1

    return (current_position, skip_length)
  

part1()