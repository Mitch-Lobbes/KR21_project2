from typing import Set
import pandas as pd
from BayesNet import BayesNet


class FrenchPruning:

    def __init__(self):
        self._bn: BayesNet
        self._query: Set[str]
        self._evidence: dict[str, bool]

    def run(self, bn: BayesNet, query: Set[str], evidence: dict[str, bool]):

        self._bn = bn
        self._query = query
        self._evidence = evidence

        self._node_pruning()
        self._edge_pruning()

    def _node_pruning(self):

        all_nodes = set(self._bn.get_all_variables())
        evidence_nodes = set(self._evidence.keys())
        given_nodes = self._query.union(evidence_nodes)
        result = all_nodes.difference(given_nodes)
        leaf_nodes = self._get_all_leaf_nodes(all_nodes=result)
        self._bn.delete_vars(variables=leaf_nodes)

    def _edge_pruning(self):

        for edge_list in [self._bn.get_edges_outgoing_from_var(variable=le_element) for le_element in self._evidence]:

            self._bn.del_edges(edges=edge_list)

            for edge in edge_list:
                u = edge[0]
                value = self._evidence[u]
                x = edge[1]

                cpt = self._bn.get_cpt(variable=x)
                print(cpt)

                new_cpt = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(data={u: value}, index=[u]), cpt=cpt)

                self._bn.update_cpt(variable=x, cpt=new_cpt)
                cpt = self._bn.get_cpt(variable=x)
                print(cpt)



    def multi_fly(self, factors: list[pd.DataFrame]):
        all_columns = []

        set([all_columns.extend(df.columns) for df in factors])



    def _get_all_leaf_nodes(self, all_nodes: Set[str]) -> list[str]:
        """Get a list of all leaf nodes of the current graph

        Returns:
            List[str]: List of leaf nodes
        """
        # all_nodes = self.bn.get_all_variables()
        return [node for node in all_nodes if self._is_leaf_node(node)]

    def _is_leaf_node(self, node: str) -> bool:
        """Checks if given node is a leaf node -> Has no further successors

        Args:
            node (str): Node to check

        Returns:
            bool: True if it is a leaf node, False otherwise
        """
        return len(self._bn.get_children(variable=node)) == 0
