import os
import json
import time

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_affinity_graph import TaskAffinityGraph

from utils.crewmen_utils import load_all

from scheduling_algorithms.m3c.m3c import M3C

def sched_algo_log_helper(w_amt, t_amt, deps, min_netcost):
    print(f"--- Test #{1} - Workers: {w_amt} | Tasks: {t_amt} ---")
    print(f"Deployement Set (Least Net Cost):\t{deps}")
    # dep_maps: list[str] = []
    # # print(deps)
    # for d in deps:
    #     dep_maps.append(d.get_display_text())

    # print(dep_maps)

    print("Minimum Netcost: ", min_netcost, "\n")

if __name__ == "__main__":
    workers: list[Worker] = []
    links: list[Link] = []
    worker_graph = WorkerGraph()
    tasks: list[Task] = []
    task_affinity_graph = TaskAffinityGraph()
    
    with open((os.path.join("in/logs_2024-04-17_14-15-34", f"5_log.json")), 'r') as file:
        data = json.load(file)

        # Load All
        load_all(data, workers, links, worker_graph, tasks, task_affinity_graph)

        # Evaluate using Brute Force Scheduling Algorithm
        print("\n--- M3C Scheduling Algorithm ---")
        start_time = time.time()  # Record the start time

        m3c = M3C(workers, tasks, worker_graph, task_affinity_graph)
        m3c_deployment, m3c_net_cost, m3c_total_colocations = m3c.run()

        sched_algo_log_helper(len(workers), len(tasks), m3c_deployment, m3c_net_cost)     

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken: {elapsed_time} seconds\n")
