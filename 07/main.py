import re
from typing import List

import networkx as nx

from utils.log import LOG
from utils.readers import FileReader

BAGS_RULE_LINE_REGEX = re.compile(r"^(\w+ \w+) bags contain (.*).")
BAGS_RULE_COMPONENT_REGEX = re.compile(r"(\d+) (\w+ \w+) bags?")


class BagRules(FileReader):
    """
    Implementation of a bag rules file reader.

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    """

    def read(self, *args, **kwargs) -> List[dict]:
        """
        Implementation of a bag rules file read function.
        """
        data = super(BagRules, self).read()

        result = []
        # Split rules
        rules_raw = [line for line in data.split("\n") if line]

        for rule_raw in rules_raw:
            bag_color, content_raw = BAGS_RULE_LINE_REGEX.match(rule_raw).groups()
            rule_parsed = {"bag_color": bag_color, "bag_rule_components": []}
            if content_raw != "no other bags":
                bag_rule_components = []
                bag_rule_components_raw = content_raw.split(",")
                for bag_rule_component_raw in bag_rule_components_raw:
                    (
                        rule_component_count,
                        rule_component_color,
                    ) = BAGS_RULE_COMPONENT_REGEX.match(
                        bag_rule_component_raw.strip()
                    ).groups()

                    bag_rule_components.append(
                        {
                            "rule_component_count": rule_component_count,
                            "rule_component_color": rule_component_color,
                        }
                    )
                rule_parsed["bag_rule_components"] = bag_rule_components
            result.append(rule_parsed)

        return result


def count_bags_inside_a_bag(graph, color, count=0):
    """
    Given a graph and a bag color color, find the number of bags inside

    :param graph: Graph
    :param color: Bag color
    :param count: Actual count
    :return: Total count
    """
    # Graph is reversed
    edges = graph.in_edges(color)
    if not edges:
        return 1

    temp_result = 0
    for edge in edges:
        weight = graph[edge[0]][edge[1]]["weight"]
        result = int(weight) * count_bags_inside_a_bag(graph, edge[0], count)
        temp_result += result

    return count + temp_result + 1


def create_bag_graph(rules):
    """
    Given a list of rules, create an inverted directed graph representing the russion
    dolls bags.

    :param rules: Rules list
    :return:graph
    """
    graph = nx.DiGraph()

    for rule in rules:
        for rule_component in rule["bag_rule_components"]:
            graph.add_edge(
                rule_component["rule_component_color"],
                rule["bag_color"],
                weight=rule_component["rule_component_count"],
            )

    return graph


test_reader = BagRules("input-test.txt")
test_data = test_reader.read()

reader = BagRules("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)

for data_source_name, data_source in data_sources:
    graph = create_bag_graph(data_source)

    LOG.info(
        f"Day 07 result 1 - {data_source_name}: {len(nx.descendants(graph, 'shiny gold'))} "
    )

    LOG.info(
        f"Day 07 result 2 - {data_source_name}: {count_bags_inside_a_bag(graph, 'shiny gold')} "
    )
