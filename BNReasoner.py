from typing import Union, Set
import copy
from networkx import DiGraph

from BayesNet import BayesNet


class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net
            
    # UTILITY FUNCTIONS ------------------------------------------------------------------------------------------------

    def prune(self, X: Set[str], Z: Set[str], Y: Set[str]) -> DiGraph:
        """Create a pruned graph G' off G, based on the provided sets of nodes

        Args:
            X, Y, Z (Set[str]): Sets of nodes

        Returns:
            DiGraph: Pruned graph
        """

        leaf_nodes = self.get_all_leaf_nodes()
        union_set = X.union(Y).union(Z)

        g_prime = copy.deepcopy(self.bn)

        # Remove all leaf nodes W ∉ XuYuZ and delete edges ingoing to W
        for leaf_node in leaf_nodes:
            if leaf_node not in union_set:
                g_prime.del_var(variable=leaf_node)
                self.bn.del_edges(self.bn.get_edges_ingoing_to_var(variable=leaf_node))


        # Remove all edges outgoing from Z
        for node in Z:
            self.bn.del_edges(self.bn.get_edges_outgoing_from_var(variable=node))

        return g_prime



    def prune_leaf_nodes_not_in_set(self ):
        pass

    def get_all_leaf_nodes(self) -> list[str]:
        """Get a list of all leaf nodes of the current graph

        Returns:
            List[str]: List of leaf nodes
        """
        all_nodes = self.bn.get_all_variables()
        return [node for node in all_nodes if self._is_leaf_node(node)]
    
    def _is_leaf_node(self, node: str) -> bool:
        """Checks if given node is a leaf node -> Has no further successors

        Args:
            node (str): Node to check

        Returns:
            bool: True if it is a leaf node, False otherwise
        """
        return len(self.bn.get_children(variable=node)) == 0
            
    # Task 1: Developing a Bayesian Network Reasoner -------------------------------------------------------------------
    def d_separation(self, X: Set[str], Y: Set[str], Z: Set[str]) -> bool:
        """Determins whether X is independent of Y, given Z

        Args:
            X (str): [description]
            Y (str): [description]
            Z (str): [description]

        Returns:
            bool: [description]
        """
        pass
    
    def _pruning(self, X: str, Y: str, Z:str) -> None:
        """Delete every leaf node W ∉ X∪Y∪Z
        """
        pass

    # TODO: This is where your methods should go
