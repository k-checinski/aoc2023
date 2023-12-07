from collections import Counter
from dataclasses import dataclass
from functools import cmp_to_key
from typing import Literal

p1_ordering = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
p2_ordering = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
p1_ordering.reverse()
p2_ordering.reverse()

n_cards = len(p1_ordering)

handprint_types = [
    (5,),
    (1, 4),
    (2, 3),
    (1, 1, 3),
    (1, 2, 2),
    (1, 1, 1, 2),
    (1, 1, 1, 1, 1)
]
handprint_types.reverse()

type Card = Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
type Hand = tuple[Card, Card, Card, Card, Card]




@dataclass
class Row:
    hand: Hand
    bid: int
    #
    # def __post_init__(self):
    #     self.hand = tuple(reversed(sorted(self.hand, key=get_card_strength)))


def get_card_strength(card: Card) -> int:
    return p2_ordering.index(card)


def get_hand_cards_strength(hand: Hand) -> int:
    return sum(i ** n_cards * get_card_strength(card) for i, card in enumerate(reversed(hand), 1))


def get_type_strength(hand: Hand) -> int:
    handprint = get_handprint(hand)
    return handprint_types.index(handprint)


def compare_hands(hand1: Hand, hand2: Hand) -> int:
    type_strength1 = get_type_strength(hand1)
    type_strength2 = get_type_strength(hand2)
    if type_strength1 != type_strength2:
        return type_strength1 - type_strength2
    return get_hand_cards_strength(hand1) - get_hand_cards_strength(hand2)


def compare_rows(row1: Row, row2: Row) -> int:
    return compare_hands(row1.hand, row2.hand)


def get_handprint(hand: Hand) -> tuple[int]:
    counter = Counter(hand)
    best = max(counter, key=counter.get)
    hand2 = tuple(best if c == "J" else c for c in hand)
    if hand != hand2:
        print(hand, tuple(sorted(Counter(hand).values())), hand2, tuple(sorted(Counter(hand2).values())))
    return tuple(sorted(Counter(hand2).values()))


def parse_row(line: str) -> Row:
    hand_str, bid_str = line.split(" ", maxsplit=1)
    return Row(tuple(hand_str), int(bid_str))


def parse_input(filename: str) -> list[Row]:
    with open(filename) as file:
        return [parse_row(line) for line in file.readlines()]


def part_1(filename: str) -> int:
    rows = parse_input(filename)
    rows = sorted(rows, key=cmp_to_key(compare_rows))
    return sum(i * row.bid for i, row in enumerate(rows, 1))


def part_2(filename: str) -> int:
    rows = parse_input(filename)
    rows = sorted(rows, key=cmp_to_key(compare_rows))
    return sum(i * row.bid for i, row in enumerate(rows, 1))

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

