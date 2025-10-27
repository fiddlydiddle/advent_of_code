
def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2024/day1/input.txt', 'r').readlines()
    list1 = []
    list2 = [] # for part 1
    list2_map = {} # for part 2
    # parse input to two lists
    for line in input:
        line = line.rstrip()
        list1_item, list2_item = line.split('   ')
        list1.append(int(list1_item))
        list2.append(int(list2_item))
        # part 2 keep a map of occurrences of each num in list 2
        if list2_item in list2_map:
            list2_map[list2_item] += 1
        else:
            list2_map[list2_item] = 1

    # sort the lists
    list1.sort()
    list2.sort()

    # calculate distances and similarities
    total_distance = 0
    total_similarity_score = 0
    for idx, list1_val in enumerate(list1):
        list2_val = list2[idx]

        # Part 1: distance
        item_distance = abs(list1_val - list2_val)
        total_distance += item_distance

        # Part 2: similarity
        item_similarity = list2_map[str(list1_val)] if str(list1_val) in list2_map else 0
        total_similarity_score += (list1_val * item_similarity)

    print(f"Part 1 Distance: {total_distance}")
    print(f"Part 2 Similarity: {total_similarity_score}")

main()