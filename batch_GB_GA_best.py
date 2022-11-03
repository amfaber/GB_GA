#!/bin/env python
#SBATCH --job-name=batch_GA_best
#SBATCH --time=1-00:00:00
#SBATCH -p gpu --gres=gpu:titanrtx:1
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.getcwd())
    from GB_GA import *
    import argparse
    # p = argparse.ArgumentParser()
    # p.add_argument("-i", dest = "input")
    # p.add_argument("-o", dest = "output")
    # p = p.parse_args()
    p = argparse.ArgumentParser()
    p = p.parse_args()
    p.input = "/home/qzj517/POR-DD/Enamine_library/enamine_best_1000.sdf"
    p.output = "/home/qzj517/POR-DD/GB_GA/runs/1000_best_enamine_lipinski"
    # p.input = Path(p.input)
    # p.output = Path(p.output)

    arglist = [
    "-r", "/home/qzj517/POR-DD/data/raw_data/por_structures/3QE2_1_reduced.pdb",
    "--device", "cuda:0", # if torch.cuda.is_available() else "cpu",
    "-o", p.output,
    "--batch_size", "34",
    "--addH", "--use_rdkit_coords",
    ]

    rewarder = eqr.Rewarder("vs", arglist,
    default_score = 0,
    )

    population_size = 100
    file_name = p.input
    scoring_function = rewarder
    generations = 100
    mating_pool_size = 20
    mutation_rate = 0.05
    # with mp.Pool(8) as pool:
    scoring_args = []
    max_score = 1000.
    prune_population = False
    for i in range(10):
        seed = i + 10
        if (Path(p.output) / f"results_{i}.pickle").exists():
            print(f"skipped {Path(p.output) / f'results_{i}.pickle'}")
            continue
        rewarder.gnina_save = Path(p.output) / f"all_gnina_{i}.sdf"
        rewarder.equibind_save = Path(p.output) / f"all_equibind_{i}.sdf"
        args = (population_size, file_name,scoring_function,generations,mating_pool_size,mutation_rate, \
        scoring_args, max_score, prune_population, seed)
        results = GA(args)
        with open(Path(p.output) / f"results_{i}.pickle", "wb") as file:
            pickle.dump(results, file) 