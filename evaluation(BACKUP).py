import glob, os
import random
import time

from pgmpy.readwrite import BIFReader, XMLBIFWriter

from BayesNet import BayesNet
from Ordering import Ordering
from MPE import MPE

PATH = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/Networks/**"


def load_bns() -> list[BayesNet]:
    bns = []
    for file_path in glob.iglob(PATH, recursive=True):
        if file_path.endswith("BIFXML"):  # filter dirs
            print(file_path)
            bn = BayesNet()
            bn.load_from_bifxml(file_path=file_path)
            bns.append(bn)
    return bns[1:-1]


def run_experiment():
    bns = load_bns()
    ordering = Ordering()
    mpe = MPE()

    mpe_dict = dict()

    for bn in bns:

        # Get all variables
        vars = bn.get_all_variables()

        # Get all orderings
        order_min_degree = [ordering.min_degree(bn=bn, X=vars)]
        order_min_fill = [ordering.min_fill(bn=bn, X=vars)]
        random_orderings = ordering.random_orderings(X=vars, heuristic_orders=[order_min_degree[0], order_min_fill[0]])

        orderings = [order_min_degree, order_min_fill, random_orderings]
        evidence_var = {random.choice(vars): True}

        for idx, orderingg in enumerate(orderings):
            heuristic = "order_min_degree" if idx == 0 else "order_min_fill" if idx == 1 else "random"
            print(f"Heuristic being used: {heuristic}")
            total_time = 0

            for order in orderingg:
                print(order)
                time_before = time.time()
                mpe.run(
                    bn=bn,
                    evidence=evidence_var,
                    order=order
                )
                runtime = time.time() - time_before
                total_time += runtime
            time_avg = total_time / len(orderingg)

            if heuristic not in mpe_dict.keys():
                key_value = f"{idx}_Variables{len(vars)}"
                mpe_dict[heuristic] = {
                    key_value: time_avg
                }
            else:
                key_value = f"{idx}_Variables{len(vars)}"
                mpe_dict[heuristic][key_value] = time_avg
    return mpe_dict


if __name__ == "__main__":
    d = run_experiment()
    for k, v in d.items():
        print(k, v)

