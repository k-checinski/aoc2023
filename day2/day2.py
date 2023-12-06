from typing import TypeAlias
from functools import reduce
from operator import mul

CubeSet: TypeAlias = dict[str, int]
Game: TypeAlias = list[CubeSet]


def parse_pair(s: str) -> tuple[str, int]:
    split = s.split(" ", maxsplit=1)
    return split[1], int(split[0])


def parse_cubes_set(s: str) -> CubeSet:
    pairs_str = s.split(", ")
    return dict(parse_pair(pair) for pair in pairs_str)


def parse_game(s: str) -> Game:
    game = s.split(": ", 1)[1]
    return [parse_cubes_set(st.strip()) for st in game.split("; ")]


def parse_input(filename: str) -> list[Game]:
    with open(filename) as file:
        lines = file.readlines()
    return [parse_game(line.strip()) for line in lines]


def get_cubes(cube_set: CubeSet, color: str) -> int:
    return cube_set.get(color, 0)


def is_set_possible(set_1: CubeSet, set_2: CubeSet) -> bool:
    return all(set_1[color] >= get_cubes(set_2, color) for color in set_1.keys())


def is_game_possible(cube_set: CubeSet, game: Game) -> bool:
    return all(is_set_possible(cube_set, game_set) for game_set in game)


def get_greater_set(set_1: CubeSet, set_2: CubeSet) -> CubeSet:
    present_colors = set(list(set_1.keys()) + list(set_2.keys()))
    return {
        color: max(get_cubes(set_1, color), get_cubes(set_2, color))
        for color in present_colors
    }


def part_1(filename: str) -> int:
    question_set = CubeSet({"red": 12, "green": 13, "blue": 14})
    games = parse_input(filename)
    return sum(
        i for i, game in enumerate(games, 1) if is_game_possible(question_set, game)
    )


def get_minimal_set(game: Game) -> CubeSet:
    return reduce(get_greater_set, game)


def get_set_power(cube_set: CubeSet) -> int:
    return reduce(mul, cube_set.values())


def part_2(filename: str) -> int:
    games = parse_input(filename)
    min_sets = [get_minimal_set(game) for game in games]
    sets_power = [get_set_power(s) for s in min_sets]
    return sum(sets_power)


def main():
    p1_test_answer = part_1("test.txt")
    p1_answer = part_1("input.txt")

    print(f"{p1_test_answer=}")
    print(f"{p1_answer=}")

    p2_test_answer = part_2("test.txt")
    p2_answer = part_2("input.txt")

    print(f"{p2_test_answer=}")
    print(f"{p2_answer=}")


if __name__ == "__main__":
    main()
