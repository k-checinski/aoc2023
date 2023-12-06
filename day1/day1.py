def read_data(filename):
    with open(filename) as file:
        return file.readlines()


def get_coordinates(line: str) -> int:
    a = next(filter(str.isdigit, line))
    b = next(filter(str.isdigit, reversed(line)))
    return int(a + b)


digits = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def find_first_occurred_value_idx(line: str, values: list[str]) -> int:
    pos = [line.find(v) for v in values]
    return min(enumerate(pos), key=lambda x: x[1] if x[1] >= 0 else float("inf"))[0]


def find_last_occurred_value_index(line: str, values: list[str]) -> int:
    pos = [line.rfind(v) for v in values]
    return max(enumerate(pos), key=lambda x: x[1])[0]


def find_first_digit(line) -> int:
    first_digit = find_first_occurred_value_idx(line, digits)
    return first_digit % 10


def find_last_digit(line) -> int:
    last_digit = find_last_occurred_value_index(line, digits)
    return last_digit % 10


def get_spelled_coordinates(line: str) -> int:
    f_digit = find_first_digit(line)
    l_digit = find_last_digit(line)
    coordinates = f_digit * 10 + l_digit
    # print(coordinates)
    return coordinates


def part1(filename):
    lines = read_data(filename)
    return sum(get_coordinates(line) for line in lines)


def part2(filename):
    lines = read_data(filename)
    return sum(get_spelled_coordinates(line) for line in lines)


def main():
    test_answer = part1("test.txt")
    answer = part1("input.txt")
    print("example", test_answer)
    print("input", answer)

    test_p2_answer = part2("test2.txt")
    p2_answer = part2("input.txt")
    print(test_p2_answer)
    print(p2_answer)


if __name__ == "__main__":
    main()
