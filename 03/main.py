from typing import List

from utils.log import LOG
from utils.math import multiply
from utils.readers import FileReader


class GeologyMapReader(FileReader):
    """
    Implementation of a geology map file reader.

    E.g.

    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
    """

    def read(self, *args, **kwargs) -> List[str]:
        """
        Implementation of a geology map file read function.
        """
        data = super(GeologyMapReader, self).read()
        return [line for line in data.splitlines() if line]


test_reader = GeologyMapReader("input-test.txt")
test_data = test_reader.read()

reader = GeologyMapReader("input.txt")
prod_data = reader.read()

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def traverse_map(map_data: List[str], starting_point: List[int], vector: List[int]):
    """
    Traverse a map given a starting point and a descent vector

    :param map_data: Map list of list
    :param starting_point: Starting point coordinates
    :param vector: Y, X vector, in direction of the bottom right corner of the X,Y axis
    :return: Number of tree impacted
    """
    first = True
    max_y = len(map_data)
    max_x = len(map_data[0])
    current_point = starting_point
    tree_impacted = 0

    # Use the y vector to determine the number of steps needed to traverse the map
    for _ in range(int(max_y / vector[0]) + 1):
        if not first:
            # Ensure the y vector won't step out of bounds
            current_x = (current_point[1] + vector[1]) % max_x
            if current_point[0] + vector[0] >= max_y:
                current_point = [max_y - 1, current_x]
            else:
                current_point = [current_point[0] + vector[0], current_x]

        if map_data[current_point[0]][current_point[1]] == "#":
            tree_impacted += 1

        first = False

    return tree_impacted


for data_source_name, data_source in data_sources:
    tree_impacted = traverse_map(data_source, [0, 0], [1, 3])
    LOG.info(f"Day 0 result 1 - {data_source_name}: {tree_impacted}")

    slope_vectors = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]
    slopes_results = []
    for slope_vector in slope_vectors:
        tree_impacted = traverse_map(data_source, [0, 0], slope_vector)
        slopes_results.append(tree_impacted)

    LOG.info(f"Day 0 result 2 - {data_source_name}: {multiply(slopes_results)}")
