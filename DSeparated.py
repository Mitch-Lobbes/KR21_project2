from typing import Set
import copy

from networkx import DiGraph

from BayesNet import BayesNet


class DSeparated:

    def __init__(self):
        self.bayesNet: BayesNet
        self.X: Set[str]
        self.Z: Set[str]
        self.Y: Set[str]

    def d_separated(self, bayesNet: BayesNet, X: Set[str], Z: Set[str], Y: Set[str]) -> bool:
        self.bayesNet = copy.deepcopy(bayesNet)
        self.X = X
        self.Z = Z
        self.Y = Y

        # Step 1: Ancestral Graph
        self._ancestral_graph()

        # Step 2: Moralization
        self._moralization()

        # Step 3: Givens Removal
        self._given_removal()

        # Step 4: Check if path exists
        for node in self.X:
            connected_nodes = self._connected_nodes(wanted_node=node)
            for y_node in self.Y:
                if y_node in connected_nodes:
                    return False

        return True

    def _connected_nodes(self, wanted_node: str) -> Set[str]:
        connection_dict = {}
        for node in self.bayesNet.structure.nodes:
            neighbors = self.bayesNet.get_neighbors(node=node)
            connection_dict[node] = set(neighbors)

        done = False
        while not done:
            len_before = len(connection_dict[wanted_node])
            new_connections = copy.deepcopy(connection_dict[wanted_node])
            for connected_node in connection_dict[wanted_node]:
                node_neioghbors = connection_dict[connected_node]
                new_connections = new_connections.union(node_neioghbors)
            connection_dict[wanted_node] = new_connections
            if len_before == len(new_connections):
                done = True

        return connection_dict[wanted_node]

    # KILL unimportant nodes
    def _ancestral_graph(self) -> None:
        union_set = self.X.union(self.Y).union(self.Z)
        done = False
        while not done:
            amount_vars_before = len(self.bayesNet.get_all_variables())
            leaf_nodes = self.bayesNet.get_all_leaf_nodes()
            # Remove all leaf nodes W ∉ XuYuZ and delete edges ingoing to W
            for leaf_node in leaf_nodes:
                if leaf_node not in union_set:
                    self.bayesNet.del_var(variable=leaf_node)
                    self.bayesNet.del_edges(self.bayesNet.get_edges_ingoing_to_var(variable=leaf_node))
            if amount_vars_before == len(self.bayesNet.get_all_variables()):
                done = True

    def _moralization(self) -> None:
        for node in self.Z:
            parents = self.bayesNet.structure.predecessors(node)
            parents = list(parents)
            # Marry parents
            for i in range(len(parents)):
                if i+1 == len(parents):
                    break
                for j in range(i+1, len(parents)):
                    edge = (parents[i], parents[j])
                    self.bayesNet.add_edge(edge=edge)

    def _given_removal(self) -> None:
        for node in self.Z:
            edges = self.bayesNet.get_edges_for_var(variable=node)
            self.bayesNet.del_edges(edges=edges)
            self.bayesNet.del_var(variable=node)

