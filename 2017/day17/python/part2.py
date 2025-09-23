class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def insert(node, val):
    # before: node -> former_next
    # after:  node -> new_next -> former_next
    former_next = node.next
    new_next = Node(val)
    node.next = new_next
    new_next.next = former_next

def part2(num_steps_per_iteration, num_iterations):
    # Initalize linked list with 1 node whose value is 0
    current_node = Node(0)
    current_node.next = current_node
    first_node = current_node # Part 2, keep reference to initial node for after steps are complete

    # Perform steps and insertions the required number of iterations
    for value_to_insert in range(1, num_iterations + 1):
        # take required steps
        next_node = current_node
        for _ in range(num_steps_per_iteration):
            next_node = next_node.next

        # insert new node and step to it
        insert(next_node, value_to_insert)
        current_node = next_node.next

    # take final step and return
    current_node = current_node.next
    return current_node.val, first_node.next.val

def part2_optimized(num_steps_per_iteration, num_iterations):
    current_position = 0
    result = 0
    for val_to_insert in range(1, num_iterations + 1):
        current_position = (current_position + num_steps_per_iteration) % val_to_insert
        if current_position == 0:
            result = val_to_insert
        current_position += 1

    return result

#print(part2(3, 2017)[0]) # part 1 test from example, should return 638
#print(part2(304, 2017)[0])
#print(part2(304, 50_000_000)[1]) # This will take a LOOOOOONG  time
print(part2_optimized(304, 50_000_000))