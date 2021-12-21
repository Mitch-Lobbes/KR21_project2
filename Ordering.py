import random
import copy
from networkx import DiGraph, Graph

from BayesNet import BayesNet
from itertools import permutations


class Ordering:

    def __init__(self):
        pass

    def min_degree(self, bn: BayesNet , X: list[str]) -> list[str]:
        X = copy.deepcopy(X)
        interaction_graph = bn.get_interaction_graph()
        order = []

        for i in range(len(X)):
            node = self._get_node_with_smallest_nbr_neighbors(interaction_graph=interaction_graph, X=X)
            self._connect_edges_between_non_adjacent_neighbors(interaction_graph=interaction_graph, node=node)
            interaction_graph.remove_node(n=node)
            X.remove(node)
            order.append(node)
            
        return order

    def min_fill(self, bn: BayesNet, X: list[str]) -> list[str]:
        X = copy.deepcopy(X)
        interaction_graph = bn.get_interaction_graph()
        order = []

        for i in range(len(X)):
            node = self._return_node_with_smallest_hypo_edge(interaction_graph=interaction_graph, X=X)
            self._connect_edges_between_non_adjacent_neighbors(interaction_graph= interaction_graph, node = node)
            interaction_graph.remove_node(n=node)
            X.remove(node)
            order.append(node)

        return order

    @staticmethod
    def random_orderings(X: list[str], heuristic_orders: list[list[str]], amount: int) -> list[list[str]]:

        while len(heuristic_orders) < amount + 2:

            r = random.sample(X, len(X))

            if r not in heuristic_orders:
                heuristic_orders.append(r)


        return heuristic_orders[2:]

    def _get_node_with_smallest_nbr_neighbors(self, interaction_graph: Graph, X: list[str]) -> str:
        node = X[0]
        least_amount_neighbors = len(list(interaction_graph.neighbors(X[0])))
        for i in range (1, len(X)):
            amount_neighbors = len(list(interaction_graph.neighbors(X[i])))
            if amount_neighbors < least_amount_neighbors:
                node = X[i]
                least_amount_neighbors = amount_neighbors
        return node

    def _connect_edges_between_non_adjacent_neighbors(self, interaction_graph: Graph, node: str) -> None:
        neighbors = list(interaction_graph.neighbors(node))
        for i in range(len(neighbors)):
            neighbors_i = list(interaction_graph.neighbors(neighbors[i]))
            if i+1 == len(neighbors):
                break
            for j in range(i+1, len(neighbors)):
                if neighbors[j] not in neighbors_i:
                    interaction_graph.add_edge(neighbors[i], neighbors[j])

    def _return_node_with_smallest_hypo_edge(self, interaction_graph: Graph, X: list[str]) -> str:
        return sorted(X, key=lambda x: self._hypo_edge(interaction_graph=interaction_graph, node=x))[0]

    def _hypo_edge(self, interaction_graph: Graph, node: str) -> None:
        neighbors = list(interaction_graph.neighbors(node))
        edges_added = 0
        for i in range(len(neighbors)):
            neighbors_i = list(interaction_graph.neighbors(neighbors[i]))
            if i+1 == len(neighbors):
                break
            for j in range(i+1, len(neighbors)):
                if neighbors[j] not in neighbors_i:
                    edges_added += 1
        return edges_added
