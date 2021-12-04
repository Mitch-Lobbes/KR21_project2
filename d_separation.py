from typing import Set

from networkx import DiGraph

from BayesNet import BayesNet


class DSeparated:

    def __init__(self):
        self.bayesNet: BayesNet
        self.X: Set[str]
        self.Z: Set[str]
        self.Y: Set[str]

    def d_separated(self, bayesNet: BayesNet, X: Set[str], Z: Set[str], Y: Set[str]) -> bool:
        self.bayesNet = bayesNet
        self.X = X
        self.Z = Z
        self.Y = Y

        # Step 1: Ancestral Graph
        self._ancestral_graph()

        # Step 2: Moralization
        self._moralization()

        # Step 3:

        pass

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
        for node in self.bayesNet.get_all_variables():
            parents = self.bayesNet.structure.predecessors(node)
            # Marry parents
            for i in range(len(parents)):
                if i+1 == len(parents):
                    break
                for j in range(i+1, len(parents)):
                    edge = (parents[i], parents[j])
                    self.bayesNet.add_edge(edge=edge)


    def prune(self) -> None:
        pass
