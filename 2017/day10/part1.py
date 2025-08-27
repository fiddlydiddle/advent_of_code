num_list = [i for i in range(256)]

input_twists = [31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33]

def hash_string(string, twists):
    current_position = 0
    skip_length = 0

    for length in twists:
        starting_position = current_position
        ending_position = starting_position + length - 1

        # Perform "twist" by swapping starting and ending characters
        # Take mod(length of list) to handle wrapping
        while starting_position < ending_position:
            
            string[starting_position % len(string)], string[ending_position % len(string)] = string[ending_position % len(string)], string[starting_position % len(string)]

            starting_position += 1
            ending_position -= 1

        current_position = (current_position + length + skip_length) % len(string)
        skip_length += 1

    print(num_list[0] * num_list[1])

hash_string(num_list, input_twists)