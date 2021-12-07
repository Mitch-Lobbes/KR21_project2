from typing import Set

from BayesNet import BayesNet

class FrenchPruning:

    def __init__(self):
        self._bn: BayesNet
        self._query: Set[str]
        self._evidence: dict[str, bool]


    def run(self,bn: BayesNet, query: Set[str], evidence: dict[str, bool]):

        self._bn = bn
        self._query = query
        self._evidence = evidence

        all_nodes = set(bn.get_all_variables())
        evidence_nodes = set(evidence.keys())
        given_nodes = query.union(evidence_nodes)
        result = all_nodes.difference(given_nodes)
        leaf_nodes = self._get_all_leaf_nodes(all_nodes=result)

        self._bn.del_var(variable="")


    def _get_all_leaf_nodes(self, all_nodes: Set[str]) -> list[str]:
        """Get a list of all leaf nodes of the current graph

        Returns:
            List[str]: List of leaf nodes
        """
        #all_nodes = self.bn.get_all_variables()
        return [node for node in all_nodes if self._is_leaf_node(node)]

    def _is_leaf_node(self, node: str) -> bool:
        """Checks if given node is a leaf node -> Has no further successors

        Args:
            node (str): Node to check

        Returns:
            bool: True if it is a leaf node, False otherwise
        """
        return len(self.bn.get_children(variable=node)) == 0
