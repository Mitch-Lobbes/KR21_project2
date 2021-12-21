import random
import os
from time import time
from BayesNet import BayesNet
from Ordering import Ordering
from MPE import MPE
import BN_Generator as BNG


class Evaluation:

    def __init__(self):
        self._pad = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/UseCase"
        self._ordering = Ordering()
        self._mpe = MPE()
        self._mpe_dict: dict

    def start_evaluation(self):

        for filename in os.listdir(self._pad):

            # Initialize BayesNet
            bn = BayesNet()
            file_path = os.path.join(self._pad, filename)
            bn.load_from_bifxml(file_path=file_path)

            # Get all variables
            variables = bn.get_all_variables()

            # Get all orderings
            order_min_degree = self._ordering.min_degree(bn=bn, X=variables)
            order_min_fill = self._ordering.min_fill(bn=bn, X=variables)
            order_random = self._ordering.random_orderings(X=variables,
                                                           heuristic_orders=[order_min_degree, order_min_fill],
                                                           amount=5040)

            # Store all orders
            all_orders = [("Degree", [order_min_degree]*5040), ("Fill", [order_min_fill]*5040), ("Random", order_random)]

            # Generate random evidence
            #evidence = {random.choice(variables): True}
            evidence = {"Obesity": True,
                        "Parental Obesity": True}

            for name, ordering in all_orders:

                total_time = 0
                counter = 0
                for order in ordering:
                    print(counter)
                    counter +=1
                    start = time()
                    self._mpe.run(bn=bn, evidence=evidence, order=order)
                    runtime = time() - start
                    total_time += runtime

                average_run_time = total_time / len(ordering)

                print(f"File: {filename}")
                print(f"Heuristic: {name}")
                print(f"# Variables: {len(variables)}")
                print(f"Runtime: {average_run_time}")
                print("------------------------------------------------------------")

    def start_evaluation2(self):

        max_nodes = 100

        for i in range(5, max_nodes, 5):

            cpt_dict, all_nodes, all_edges = BNG.bn_creator(i)

            all_nodes = list(map(str, all_nodes))
            all_edges = [tuple(map(str, tup)) for tup in all_edges]
            #print(cpt_dict['1'])


            bn = BayesNet()
            bn.create_bn(cpts=cpt_dict,edges=all_edges,variables=all_nodes)

            # Get all variables
            variables = bn.get_all_variables()

            # Get all orderings
            order_min_degree = self._ordering.min_degree(bn=bn, X=variables)
            order_min_fill = self._ordering.min_fill(bn=bn, X=variables)
            order_random = self._ordering.random_orderings(X=variables,
                                                           heuristic_orders=[order_min_degree, order_min_fill],
                                                           amount=50)

            # Store all orders
            all_orders = [("Degree", [order_min_degree]*50), ("Fill", [order_min_fill]*50), ("Random", order_random)]

            # Generate random evidence
            evidence = {random.choice(variables): True}

            for name, ordering in all_orders:

                total_time = 0
                for order in ordering:
                    start = time()
                    self._mpe.run(bn=bn, evidence=evidence, order=order)
                    runtime = time() - start
                    total_time += runtime

                average_run_time = total_time / len(ordering)
                print(f"File: Example Generator {i} Nodes")
                print(f"Heuristic: {name}")
                print(f"# Variables: {len(variables)}")
                print(f"Runtime: {average_run_time}")
                print("------------------------------------------------------------")


if __name__ == "__main__":
    evaluation = Evaluation()
    evaluation.start_evaluation()
