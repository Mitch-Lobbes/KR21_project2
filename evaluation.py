import glob, os
import random
import time

from pgmpy.readwrite import BIFReader, XMLBIFWriter

from BayesNet import BayesNet
from Ordering import Ordering
from MPE import MPE

PATH = "/Users/robinbux/Desktop/Vrije Universiteit/Period_2/KnowledgeRepresentation/Assignment/Assignment2/code/KR21_project2/Networks/**"


def load_bns() -> list[BayesNet]:
    bns = []
    for file_path in glob.iglob(PATH, recursive=True):
        if file_path.endswith("BIFXML"):  # filter dirs
            bn = BayesNet()
            bn.load_from_bifxml(file_path=file_path)
            bns.append(bn)
    return bns

def run_experiment():
    bns = load_bns()
    ordering = Ordering()
    mpe = MPE()
    mpe_dict = dict()
    for bn in bns:
        vars = bn.get_all_variables()
        order_min_degree = [ordering.min_degree(bn=bn,X=vars)]
        order_min_fill = [ordering.min_fill(bn=bn,X=vars)]
        random_orderings = ordering.random_orderings(X=vars, amount=20)
        orderings = [order_min_degree, order_min_fill, random_orderings]
        evidence_var = {random.choice(vars): True}
        for idx, ordering in enumerate(orderings):
            heuristic = "order_min_degree" if idx == 0 else "order_min_fill" if idx == 1 else "random"
            total_time = 0
            for order in ordering:
                time_before = time.time()
                mpe.run(
                    bn=bn,
                    evidence=evidence_var,
                    order=order
                )
                runtime = time.time() - time_before
                total_time += runtime
            time_avg = total_time / len(ordering)
            if not mpe_dict[heuristic]:
                mpe_dict[heuristic] = {
                    len(vars): time_avg
                }
            else:
                mpe_dict[heuristic][len(vars)] = time_avg
    return mpe_dict


if __name__ == "__main__":
    run_experiment()

