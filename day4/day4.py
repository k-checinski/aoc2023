from collections import defaultdict
from dataclasses import dataclass
import re


@dataclass
class Card:
    winning: set[int]
    owned: set[int]

    def owned_winning(self) -> set[int]:
        return self.winning.intersection(self.owned)

    def count_winning_numbers(self) -> int:
        return len(self.owned_winning())

    def points(self) -> int:
        return int(2 ** (self.count_winning_numbers() - 1))


def parse_numbers_set(line: str) -> set[int]:
    return set(int(v) for v in re.findall(r"\d+", line))


def parse_card(line: str) -> Card:
    numbers = line.split(":", 1)[1]
    winning, owned = numbers.split(" | ", 1)
    return Card(
        winning=parse_numbers_set(winning),
        owned=parse_numbers_set(owned)
    )


def load_input(filename: str) -> list[Card]:
    with open(filename) as file:
        return [parse_card(line) for line in file.readlines()]


def part_1(filename: str) -> int:
    cards = load_input(filename)
    return sum(card.points() for card in cards)


def count_copies(copies: dict[int, int]) -> int:
    return sum(copies.values())


def part_2(filename: str) -> int:
    cards = load_input(filename)
    copies = {i: 1 for i in range(len(cards))}

    for i, card in enumerate(cards):
        n_winning = card.count_winning_numbers()
        for j in range(n_winning):
            copies[i + j + 1] += copies[i]

    return count_copies(copies)

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
