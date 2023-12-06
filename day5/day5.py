import re
from dataclasses import dataclass
from functools import reduce
from typing import Optional, Self


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    @classmethod
    def from_end(cls, end: int, length: int) -> Self:
        start = end - length + 1
        return Range(start, length)

    @classmethod
    def from_borders(cls, start: int, end: int) -> Self:
        length = end - start + 1
        return Range(start, length)

    def is_valid(self) -> bool:
        return self.length > 0


@dataclass
class MappingRange:
    start_b: int
    start_a: int
    length: int

    @property
    def source_range(self) -> Range:
        return Range(self.start_a, self.length)

    def map_value(self, a: int) -> Optional[int]:
        shift = a - self.start_a
        if 0 <= shift < self.length:
            return self.start_b + shift
        return None

    def map_range(self, r: Range) -> tuple[list[Range], list[Range]]:
        mapping_r = self.source_range

        remaining_before = Range(r.start, min(mapping_r.start - r.start, r.length))
        remaining_after = Range.from_end(r.end, min(r.end - mapping_r.end, r.length))

        remaining = [remaining_before, remaining_after]
        remaining = [r for r in remaining if r.is_valid()]

        to_map = Range.from_borders(
            max(r.start, mapping_r.start), min(r.end, mapping_r.end)
        )

        if not to_map.is_valid():
            return [], remaining

        mapped_start = self.map_value(to_map.start)
        mapped_end = self.map_value(to_map.end)

        mapped_r = Range.from_borders(mapped_start, mapped_end)

        return [mapped_r], remaining


@dataclass
class Mapping:
    ranges: list[MappingRange]

    def map(self, a: int) -> int:
        for r in self.ranges:
            b = r.map_value(a)
            if b is not None:
                return b
        return a

    def map_ranges(self, ranges: list[Range]) -> list[Range]:
        remaining = ranges
        next_remaining = []
        mapped_seed_ranges = []
        for mapping_range in self.ranges:
            for seed_range in remaining:
                mapped_range, new_remaining = mapping_range.map_range(seed_range)
                mapped_seed_ranges.extend(mapped_range)
                next_remaining.extend(new_remaining)
            remaining = next_remaining
            next_remaining = []

        mapped_seed_ranges.extend(remaining)

        return mapped_seed_ranges


@dataclass
class Almanac:
    seeds: list[int]
    maps: list[Mapping]

    @property
    def seeds_ranges(self) -> list[Range]:
        starts = self.seeds[::2]
        lengths = self.seeds[1::2]
        return [Range(a, l) for a, l in zip(starts, lengths)]

    def nearest_location(self) -> int:
        print(f"{self.seeds=}")
        locations = [self.map(seed) for seed in self.seeds]
        print(f"{locations=}")
        return min(locations)

    def nearest_ranges_location(self) -> int:
        locations_ranges = self.map_ranges(self.seeds_ranges)
        starts = [r.start for r in locations_ranges]
        return min(starts)

    def map(self, seed: int) -> int:
        return reduce(self._map_value, self.maps, seed)

    def map_ranges(self, ranges: list[Range]) -> list[Range]:
        return reduce(self._map_ranges, self.maps, ranges)

    @staticmethod
    def _map_value(val: int, mapping: Mapping) -> int:
        return mapping.map(val)

    @staticmethod
    def _map_ranges(ranges: list[Range], mapping: Mapping) -> list[Range]:
        return mapping.map_ranges(ranges)


def parse_seeds(line: str) -> list[int]:
    values = re.findall(r"\d+", line)
    return [int(v) for v in values]


def is_ranges_line(line: str) -> bool:
    return line[0].isdigit()


def parse_mapping_range(line: str) -> MappingRange:
    start_b, start_a, length = re.findall(r"\d+", line)[:3]
    return MappingRange(int(start_b), int(start_a), int(length))


def parse_mapping(lines: list[str]) -> Mapping:
    return Mapping([parse_mapping_range(line) for line in lines])


def parse_mappings(lines: list[str]) -> list[Mapping]:
    mapping_lines = []
    mappings = []

    for line in lines:
        if is_ranges_line(line):
            mapping_lines.append(line)
        else:
            if len(mapping_lines) > 0:
                mapping = parse_mapping(mapping_lines)
                mapping_lines = []
                mappings.append(mapping)

    if len(mapping_lines) > 0:
        mapping = parse_mapping(mapping_lines)
        mappings.append(mapping)
    return mappings


def load_input(filename: str) -> Almanac:
    with open(filename) as file:
        seeds = parse_seeds(file.readline())
        mappings = parse_mappings(file.readlines())
    return Almanac(seeds, mappings)


def part_1(filename: str) -> int:
    almanac = load_input(filename)
    return almanac.nearest_location()


def part_2(filename: str) -> int:
    almanac = load_input(filename)
    return almanac.nearest_ranges_location()


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
