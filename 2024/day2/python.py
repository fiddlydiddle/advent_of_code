def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2024/day2/input.txt', 'r').readlines()

    part1_safe_reports = 0
    part2_safe_reports = 0
    for line in input:
        line = line.rstrip()
        levels  = line.split(' ')
        part1_safe_reports += 1 if process_report_part1(levels) else 0
        part2_safe_reports += 1 if process_report_part2(levels) else 0

    print(f"Part 1 Safe Reports: {part1_safe_reports}")
    print(f"Part 2 Safe Reports: {part2_safe_reports}")

# Returns 0 if report is unsafe and 1 if report is safe
def process_report_part1(levels):
    direction = 1 if int(levels[-1]) >= int(levels[0]) else -1
    for idx, level in enumerate(levels):
        if idx > 0:
            difference = int(level) - int(levels[idx - 1])
            
            # Check for invalid level difference
            if abs(difference) < 1 or abs(difference) > 3:
                return False
            
            # Check for invalid direction
            # Condition 1: Should be increasing but decreased
            # Condition 2: should be decreasing but increased
            if (direction == 1 and difference < direction) or (direction == -1 and difference > direction):
                return False
        
    # if we got this far, report is safe
    return True

# Returns 0 if report is unsafe and 1 if report is safe
def process_report_part2(levels):
    is_safe = process_report_part1(levels)
    if is_safe:
        return True
    else:
        for i in range(len(levels)):
            shortened_levels = levels[:i] + levels[i + 1:]
            if process_report_part1(shortened_levels):
                return True
            
    return False

main()