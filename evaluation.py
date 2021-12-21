import random
import os
from time import time
from BayesNet import BayesNet
from Ordering import Ordering
from MPE import MPE
from MAP import MAP
import BN_Generator as BNG


class Evaluation:

    def __init__(self):
        self._pad = "/Users/robinbux/Desktop/Vrije Universiteit/Period_2/KnowledgeRepresentation/Assignment/Assignment2/code/KR21_project2/UseCase"
        self._ordering = Ordering()
        self._mpe = MPE()
        self._mpe_dict: dict

        self._map_dict: dict

    def start_evaluation(self):

        for filename in os.listdir(self._pad):

            # Initialize BayesNet
            bn = BayesNet()
            file_path = os.path.join(self._pad, filename)
            bn.load_from_bifxml(file_path=file_path)

            self._map = MAP(bn=bn)

            # Get all variables
            variables = bn.get_all_variables()

            # Generate query variables
            M = {"Obesity"}

            # Generate random evidence
            evidence = {"Parental Obesity": True,
                        "Healthy Lifestyle": True
                        }

            # "Healthy Lifestyle"

            # Get all orderings
            order_min_degree = self._ordering.min_degree(bn=bn, X=variables)
            order_min_fill = self._ordering.min_fill(bn=bn, X=variables)
            order_random = self._ordering.random_orderings(X=variables,
                                                           heuristic_orders=[order_min_degree, order_min_fill],
                                                           amount=1)

            order_min_degree = list(set(order_min_degree) - M)
            order_min_degree.extend(M)

            order_min_fill = list(set(order_min_fill) - M)
            order_min_fill.extend(M)

            for order in order_random:
                order = list(set(order) - M)
                order.extend(M)

            # Store all orders
            all_orders = [("Degree", [order_min_degree]*1), ("Fill", [order_min_fill]*1)]

            for name, ordering in all_orders:

                total_time = 0
                counter = 0
                for order in ordering:
                    #print(counter)
                    counter +=1
                    start = time()
                    res = self._map.MAP(M = M, E=evidence, order=order)
                    print(res)
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

            self._map = MAP(bn=bn)


            # Get all variables
            variables = bn.get_all_variables()

            # Generate query variables
            M = set(random.choices(variables, k=2))

            # Generate random evidence
            evidences = list(set(random.choices(variables, k=2)) - M)
            evidence = {key: True for key in evidences}

            # Get all orderings
            order_min_degree = self._ordering.min_degree(bn=bn, X=variables)
            order_min_fill = self._ordering.min_fill(bn=bn, X=variables)
            order_random = self._ordering.random_orderings(X=variables,
                                                           heuristic_orders=[order_min_degree, order_min_fill],
                                                           amount=20)

            order_min_degree = list(set(order_min_degree) - M)
            order_min_degree.extend(M)

            order_min_fill = list(set(order_min_fill) - M)
            order_min_fill.extend(M)

            for order in order_random:
                order = list(set(order) - M)
                order.extend(M)

            # Store all orders
            all_orders = [("Degree", [order_min_degree]*1), ("Fill", [order_min_fill]*1), ("Random", order_random)]



            for name, ordering in all_orders:

                total_time = 0
                for order in ordering:
                    start = time()
                    self._map.MAP(M=M, E=evidence, order=order)
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
    evaluation.start_evaluation2()
