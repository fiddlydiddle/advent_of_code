def check_cycles():
    input = open('../input.txt', 'r').readline()
    moves = input.split(',')
    programs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    idx = 1
    while True:
        programs = part1(programs, moves)

        if ("".join(programs) == 'abcdefghijklmnop'):
            print(idx)
            break

        idx += 1
        
def part2():
    input = open('../input.txt', 'r').readline()
    moves = input.split(',')
    programs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    modulo = 1_000_000_000 % 42 # For our inputs, the dance cycles every 42 iterations
    for i in range(modulo):
        programs = part1(programs, moves)

        if i == 0:
            print("".join(programs))

    print("".join(programs))

def part1(programs, moves):
    for move in moves:
        move_type = move[0]
        if move_type == 's':
            spin_num = int(move[1:])
            end_part = programs[-spin_num:]
            beginning_part = programs[:-spin_num]
            programs = end_part + beginning_part
        elif move_type == 'x':
            coordinates = move[1:].split('/')
            position_1 = int(coordinates[0])
            position_2 = int(coordinates[1])
            programs[position_1], programs[position_2] = programs[position_2], programs[position_1]
        elif move_type == 'p':
            coordinates = move[1:].split('/')
            char_1 = coordinates[0]
            position_1 = programs.index(char_1)
            char_2 = coordinates[1]
            position_2 = programs.index(char_2)
            programs[position_1], programs[position_2] = programs[position_2], programs[position_1]

    return programs

part2()