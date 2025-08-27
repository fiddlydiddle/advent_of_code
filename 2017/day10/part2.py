num_list = [i for i in range(256)]

input_twists = "31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33"


def hash_string(num_list, input_twists):
    twists = parse_input_twists(input_twists)
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
    print("".join(format(number, "02x") for number in dense_hash))

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

def parse_input_twists(input_twists):
    result = []
    for character in input_twists:
        ascii_val = ord(character)
        result.append(ascii_val)

    result.extend([17, 31, 73, 47, 23])

    return result

hash_string(num_list, input_twists)