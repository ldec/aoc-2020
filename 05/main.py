from typing import Tuple, List
from math import ceil, floor

from pandas import np

from utils.log import LOG
from utils.readers import OneColumnFileReader

PLANE_ROW_NUMBER = 128
PLANE_COLUMN_NUMBER = 8

test_reader = OneColumnFileReader("input-test.txt")
test_data = test_reader.read()

reader = OneColumnFileReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def get_seat_id(row: int, column: int) -> int:
    """
    Given a seat coordinates, calculate its seat id
    """
    return row * 8 + column


def dichotomic_split(lower: int, upper: int, code: str):
    """
    Given a lower and upper bound, split it in the midlle and return the new bound
    according to the code.

    :param lower: Lower bound
    :param upper: Upper bound
    :param code: Half code
    :return: New lower and upper bounds.
    """
    if code in ("F", "L"):
        return lower, lower + floor((upper - lower) / 2)
    else:
        return ceil(lower + (upper - lower) / 2), upper


def decode_boarding_pass_component(boarding_pass_component: str, max_upper: int):
    """
    Run multiple dichotomic_split on boarding_pass_component

    :param boarding_pass_component: Initial data for dichotomic_split
    :param max_upper: Initial upper bound
    :return: Exact middle
    """
    current_lower = 0
    current_upper = max_upper - 1

    for letter in boarding_pass_component:
        current_lower, current_upper = dichotomic_split(
            current_lower, current_upper, letter
        )
    assert current_lower == current_upper
    return current_lower


def decode_boarding_pass(boarding_pass: str) -> Tuple[int, int, int]:
    """
    Decode both boarding pass parts.

    :param boarding_pass: Boarding path
    :return: row, column, seat_id
    """
    row = decode_boarding_pass_component(boarding_pass[:7], PLANE_ROW_NUMBER)
    column = decode_boarding_pass_component(boarding_pass[7:], PLANE_COLUMN_NUMBER)
    seat_id = get_seat_id(row, column)

    return row, column, seat_id


def get_adjacent_seats(x, y):
    """
    Given a seat coordinate, return the coordinates of the previous and following
    seats

    :param x: Seat x coord
    :param y: Seat y cord
    :return: Previous and following seats coordinates
    """
    before_x = x
    before_y = y - 1
    after_x = x
    after_y = y + 1

    if y == PLANE_ROW_NUMBER - 1:
        after_x += 1
        after_y = 0
    elif y == 0:
        before_x -= 1
        before_y = PLANE_ROW_NUMBER - 1

    # Lazy bounds error checking
    before_seat = (before_x, before_y)
    if before_x < 0 or before_y >= PLANE_COLUMN_NUMBER:
        before_seat = None

    after_seat = (after_x, after_y)
    if after_x >= PLANE_ROW_NUMBER or after_y >= PLANE_COLUMN_NUMBER:
        after_seat = None

    return before_seat, after_seat


def find_missing_seat(seats_data: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Given a list of seat coordinates taken, return the only one with previous and after
    seats occupied

    :param seats_data: Occupied seats data coordinates
    :return:
    """
    # Create seats matrix
    ar = np.array(seats_data)
    res = np.zeros((PLANE_ROW_NUMBER, PLANE_COLUMN_NUMBER), dtype=int)
    res[ar[:, 0], ar[:, 1]] = 1

    # Find all empty seats
    empty_seats_raw = np.where(res == 0)
    empty_seats = list(zip(empty_seats_raw[0], empty_seats_raw[1]))

    # Find the only valid empty seat
    for empty_seat in empty_seats:
        before_seat, after_seat = get_adjacent_seats(*empty_seat)

        if (
            before_seat is not None
            and after_seat is not None
            and res[before_seat[0]][before_seat[1]]
            and res[after_seat[0]][after_seat[1]]
        ):
            return empty_seat


for data_source_name, data_source in data_sources:
    seats_data = []
    seats_data_without_seat_id = []
    for boarding_pass in data_source:
        current_seat_data = decode_boarding_pass(boarding_pass)
        seats_data.append(current_seat_data)
        seats_data_without_seat_id.append(current_seat_data[:2])

    LOG.info(
        f"Day 05 result 1 - {data_source_name}: {max(seats_data, key=lambda x:x[2])} "
    )

    # Do not search the missing seat for test data
    if data_source_name != "Test data":
        missing_seat = find_missing_seat(seats_data_without_seat_id)
        missing_seat_id = get_seat_id(*missing_seat)
        LOG.info(
            f"Day 05 result 2 - {data_source_name}: Seat {missing_seat}: {missing_seat_id}"
        )
