import itertools
from collections import namedtuple
from dataclasses import dataclass
import re

type Schematic = list[str]
Position = namedtuple("Position", ["y", "x"])
type Part = tuple[str, Position]


@dataclass
class Label:
    value: int
    length: int
    pos: Position


type Gear = tuple[Part, list[Label]]

part_re = re.compile(r"[^\d.]")
label_re = re.compile(r"\d+")


def build_label_adjacency_set(label: Label) -> set[Position]:
    x = label.pos.x
    y = label.pos.y
    l = label.length
    upper_row = [Position(y - 1, x - 1 + i) for i in range(l + 2)]
    center_row = [Position(y, x - 1), Position(y, x + l)]
    bottom_row = [Position(y + 1, x - 1 + i) for i in range(l + 2)]
    return set(upper_row + center_row + bottom_row)


def match_to_part(line_idx: int, match: re.Match) -> Part:
    return match.group(0), Position(line_idx, match.start())


def get_line_parts(line_idx: int, line: str) -> list[Part]:
    matches = part_re.finditer(line)
    return [match_to_part(line_idx, match) for match in matches]


def get_parts(schematic: Schematic) -> list[Part]:
    lines_parts = [get_line_parts(i, line) for i, line in enumerate(schematic)]
    return list(itertools.chain.from_iterable(lines_parts))


def match_to_label(line_idx: int, match: re.Match) -> Label:
    return Label(
        value=int(match.group(0)),
        length=len(match.group(0)),
        pos=Position(line_idx, match.start()),
    )


def get_line_labels(line_idx: int, line: str) -> list[Label]:
    matches = label_re.finditer(line)
    return [match_to_label(line_idx, match) for match in matches]


def get_labels(schematic: Schematic) -> list[Label]:
    lines_labels = [get_line_labels(i, line) for i, line in enumerate(schematic)]
    return list(itertools.chain.from_iterable(lines_labels))


def extract_parts_positions(parts: list[Part]) -> set[Position]:
    return set([part[1] for part in parts])


def load_input(filename: str) -> Schematic:
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]
    return lines


def is_label_adjacent(label: Label, positions: set[Position]) -> bool:
    return len(build_label_adjacency_set(label).intersection(positions)) > 0


def part_1(filename: str) -> int:
    schematic = load_input(filename)

    parts = get_parts(schematic)
    parts_positions = extract_parts_positions(parts)

    labels = get_labels(schematic)

    return sum(
        label.value for label in labels if is_label_adjacent(label, parts_positions)
    )

def find_part_adjacent_labels(part: Part, labels: list[Label]) -> list[Label]:
    return [label for label in labels if part[1] in build_label_adjacency_set(label)]

def is_gear_symbol(part: Part) -> bool:
    return part[0] == "*"


def part_2(filename: str) -> int:
    schematic = load_input(filename)
    parts = get_parts(schematic)
    gears = [part for part in parts if is_gear_symbol(part)]
    labels = get_labels(schematic)

    answer = 0

    for gear in gears:
        adjacent_labels = find_part_adjacent_labels(gear, labels)
        if len(adjacent_labels) != 2:
            continue
        answer += adjacent_labels[0].value * adjacent_labels[1].value

    return answer



def main():
    p1_test_answer = part_1("test.txt")
    print(f"{p1_test_answer=}")

    p1_answer = part_1("input.txt")
    print(f"{p1_answer=}")

    p2_test_answer = part_2("test.txt")
    print(f"{p2_test_answer=}")

    p2_answer = part_2("input.txt")
    print(f"{p2_answer=}")


if __name__ == "__main__":
    main()
