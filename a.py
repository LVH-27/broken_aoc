from typing import Dict, List
from collections import defaultdict


class Symbol:
    def __init__(self, character: str, row: int, col: int):
        self.character = character
        self.row = row
        self.col = col
        self.adjacent_numbers = []

    def get_adjacent_numbers(self, part_numbers):
        adjacent_rows = [self.row - 1, self.row, self.row +1]
        adjacent_cols = [self.col - 1, self.col, self.col +1]
        for row in adjacent_rows:
            for part_number in part_numbers[row]:
                part_number_cols = range(
                    part_number.col_start, part_number.col_start + len(str(part_number))
                )
                if set(adjacent_cols) & set(part_number_cols):  # intersection
                    self.adjacent_numbers.append(part_number)

    def __str__(self):
        return f"Symbol({self.character} at row {self.row}, col {self.col})"


class PartNumber:
    def __init__(self, value, row, col_start):
        self.value = value
        self.row = row
        self.col_start = col_start

    def __str__(self):
        return f"PN({self.value} ({self.row}, {self.col_start}))"

    def __repr__(self):
        return self.__str__()

input_file = "test"
with open(input_file) as f:
    lines = [line.strip() for line in f.readlines()]

# parts and symbols, stored in one list per row
part_numbers: Dict[int, List[PartNumber]] = defaultdict(list)
symbols: Dict[int, List[PartNumber]] = defaultdict(list)

for line_idx, line in enumerate(lines):
    char_idx = 0
    number_str = ""

    while char_idx < len(line):
        # Ignore periods
        if line[char_idx] == ".":
            char_idx += 1
            continue

        # Parse symbols
        if not line[char_idx].isdigit():
            symbol = Symbol(
                character=line[char_idx],
                row=line_idx,
                col=char_idx
            )
            symbols[line_idx].append(symbol)
            char_idx += 1
            continue

        # Parse numbers
        while line[char_idx].isdigit():
            number_str += line[char_idx]
            char_idx += 1
            if char_idx == len(line):
                break
        if number_str:
            part_number = PartNumber(
                value=int(number_str),
                row=line_idx,
                col_start=char_idx - len(number_str)
            )
            part_numbers[line_idx].append(part_number)


real_part_numbers = []
for line_idx, line in enumerate(lines):
    print()
    print(line)
    for symbol in symbols[line_idx]:
        symbol.get_adjacent_numbers(part_numbers)
        print(symbol)
        print(f"\t {symbol.adjacent_numbers}")
        for part_number in symbol.adjacent_numbers:
            if part_number not in real_part_numbers:
                real_part_numbers.append(part_number)

print()
print(f"Result for {input_file}: {sum([part_number.value for part_number in real_part_numbers])}")
print("Expected result:\n\ttest input: 4316\n\treal input: 532331")

