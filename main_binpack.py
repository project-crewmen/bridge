import os
import json
import time

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_affinity_graph import TaskAffinityGraph

from utils.crewmen_utils import load_all

from scheduling_algorithms.bin_pack.bin_pack import BinPack

def sched_algo_log_helper(w_amt, t_amt, deps, min_netcost, total_colocations):
    print(f"--- Test #{1} - Workers: {w_amt} | Tasks: {t_amt} ---")
    print(f"Deployement Set (Least Net Cost):\t{deps}")
    # dep_maps: list[str] = []
    # # print(deps)
    # for d in deps:
    #     dep_maps.append(d.get_display_text())

    # print(dep_maps)

    print("Minimum Netcost: ", min_netcost, "\n")
    print("Total Colocations: ", total_colocations, "\n")

if __name__ == "__main__":
    workers: list[Worker] = []
    links: list[Link] = []
    worker_graph = WorkerGraph()
    tasks: list[Task] = []
    task_affinity_graph = TaskAffinityGraph()
    
    with open((os.path.join("in", f"logs_2024-04-15_20-55-05/5_log.json")), 'r') as file:
        data = json.load(file)

        # Load All
        load_all(data, workers, links, worker_graph, tasks, task_affinity_graph)

        # Evaluate using Brute Force Scheduling Algorithm
        print("\n--- Binpack Scheduling Algorithm ---")
        start_time = time.time()  # Record the start time

        bp = BinPack(workers, tasks, worker_graph, task_affinity_graph)
        binpacked_deployment, net_cost, total_colocations = bp.run()

        sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, net_cost, total_colocations)     

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken: {elapsed_time} seconds\n")
