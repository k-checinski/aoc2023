import math
import re
from collections import namedtuple

Race = namedtuple("Race", ["time", "distance"])


def parse_input(filename: str) -> list[Race]:
    with open(filename) as file:
        times = map(int, re.findall(r"\d+", file.readline()))
        distances = map(int, re.findall(r"\d+", file.readline()))
    return [Race(t, d) for t, d in zip(times, distances)]


def parse_input_p2(filename: str) -> Race:
    with open(filename) as file:
        time = int("".join(re.findall(r"\d+", file.readline())))
        distance = int("".join(re.findall(r"\d+", file.readline())))
    return Race(time, distance)


def get_win_holding_times(race: Race) -> int:
    a1 = (race.time - math.sqrt(race.time * race.time - 4 * race.distance)) / 2
    a2 = (race.time + math.sqrt(race.time * race.time - 4 * race.distance)) / 2

    ra1 = int(math.ceil(a1))
    ra2 = int(math.floor(a2))

    if a1.is_integer():
        ra1 += 1

    if a2.is_integer():
        ra2 -= 1

    return ra2 - ra1 + 1

def part_1(filename: str) -> int:
    races = parse_input(filename)

    ns_wins = [get_win_holding_times(race) for race in races]
    print(ns_wins)
    return math.prod(ns_wins)


def part_2(filename: str) -> int:
    race = parse_input_p2(filename)
    return get_win_holding_times(race)


def main():
    p1_test_answer = part_1("test.txt")
    print(p1_test_answer)

    p1_answer = part_1("input.txt")
    print(p1_answer)

    p2_test_answer = part_2("test.txt")
    print(p2_test_answer)

    p2_answer = part_2("input.txt")
    print(p2_answer)


if __name__ == '__main__':
    main()

