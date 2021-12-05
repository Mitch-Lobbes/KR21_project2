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

        # Step 3: Givens Removal
        self._given_removal()

        pass

# keep the nodes of all three sets and their ancestors (parents, parent's parents)
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

# "marry" (connect with edges) all common parents
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

# SKIPPED => disorient graph (replace directed edges with unidirected edges)

# remove givens (Z) and their edges
    def _given_removal(self) -> None:
        for node in self.Z:
            edges = self.bayesNet.get_edges_for_var(variable=node)
            self.bayesNet.del_edges(edges=edges)
            self.bayesNet.del_var(variable=node)


# read the answer of the graph
# variables (X,Y) disconnected => d-seperated/independent
# varibles (X,Y) connected => dependent

# way to go => check if weakly connected; if no its d-seperated
# Question: do all nodes of X need to be connected to all nodoes of Y or is partially connected also?

# make recursive function that loops through edges => always with new starting node until all edges are done or it found a connection to Y
"""

start with first node in X

while not done:
    for node in X:
        next_node = node
        for tuple in reversed(all_edges_list):
            if node in tuple:
                if node == tuple[0]:
                    next_node = tuple[1]
                    all_edges_list.remove(tuple)

                    


                elif node == tuple[1]:
                    next_node = tuple[0]
                    all_edges.remove(tuple)
                    if tuple[2] in 







    else:
        return True (they are d-seperated)

"""





    def prune(self) -> None:
        pass
