import itertools
import random
import pandas as pd
import pprint


def bn_creator(number_of_nodes):
    all_nodes = list(range(1, number_of_nodes + 1))
    all_children = {int(node): [] for node in all_nodes}
    all_parents = {int(node): [] for node in all_nodes}
    all_edges = []

    for node in range(1, number_of_nodes):
        num_children = random.randint(1, 3)
        for i in range(num_children):
            child = random.randint(node + 1, number_of_nodes)
            if child in all_children[node]:
                continue
            else:
                all_children[node].append(child)
                all_parents[child].append(node)
                all_edges.append((node, child))

    cpt_dict = dict.fromkeys([str(node) for node in all_nodes])

    for parent in all_parents.keys():
        column = [str(parent)] + [str(i) for i in all_parents[parent]]
        truth = [list(value) for value in itertools.product([True, False], repeat=len(column))]
        result_cpt = pd.DataFrame(truth, columns=[str(var) for var in column])
        result_cpt['p'] = 0

        for i in range(0, len(result_cpt), 2):
            p = random.uniform(0, 1)
            result_cpt.loc[i, 'p'] = p
            result_cpt.loc[i + 1, 'p'] = 1 - p

        cpt_dict.update({str(parent): result_cpt})

    return cpt_dict, all_nodes, all_edges


# cpt_dict, all_nodes, all_edges = bn_creator(20)
# pprint.pprint(all_nodes)
# pprint.pprint(all_edges)
