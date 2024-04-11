import os
import json
import time

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_graph import TaskGraph
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import find_worker, find_link, find_task

from scheduling_algorithms.bf.bf import BruteForce

def sched_algo_log_helper(w_amt, t_amt, perms, deps, min_netcost):
    print(f"--- Test #{1} - Workers: {w_amt} | Tasks: {t_amt} ---")
    print(f"Total number of permutations:\t\t{perms}")
    print(f"Deployement Set (Least Net Cost):\t{len(deps)}")
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
    task_graph = TaskGraph()
    
    with open((os.path.join("in", f"log_2024-04-05_22-48-57.json")), 'r') as file:
        data = json.load(file)

        # Load, Validate & Construct Workers
        data_workers=data["workers"]
        for entry in data_workers:
            workers.append(Worker(id=entry["id"], cpu=entry["cpu"], memory=entry["memory"], disk=entry["disk"]))

        print("Workers loading successful")

        # Load, Validate & Construct Links
        data_links=data["links"]

        for entry in data_links:
            links.append(Link(id=entry["id"], response_time=entry["response_time"]))

        print("Links loading successful")

        # Load, Validate & Construct Worker Network
        data_worker_network=data["worker_graph"]

        k = 1
        for i in range(0, len(data_workers)):
            for j in range(i, len(data_workers)):
                print(i, j)
                if i == j:
                    worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{0}"))
                else:
                    worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{k}"))
                    k += 1

        print("Worker Graph setup successful")

        # Load, Validate & Construct Tasks
        data_tasks=data["tasks"]

        for entry in data_tasks:
            tasks.append(Task(id=entry["id"], cpu_required=entry["cpu_required"], memory_required=entry["memory_required"], disk_required=entry["disk_required"]))

        print("Task loading successful")

        # Load, Validate & Construct Deployments
        data_deployments=data["deployments"]
        
        for key, values in data_deployments.items():
            deploying_worker = find_worker(workers, key)
            for value in values:
                task_to_be_deployed = find_task(tasks, value)
                deploying_worker.deploy_task(task_to_be_deployed)

        print("Deployment successful")
    
        # Load, Validate & Construct Task Network
        data_task_network=data["task_affinity_graph"]

        for x in range(0, len(data_tasks)):
            for y in range(0, len(data_tasks)):
                if x != y:
                    # Find Tasks
                    x_task = find_task(tasks, f"t_{x}")
                    y_task = find_task(tasks, f"t_{y}")

                    # Find Affinity Cost
                    associated_affinity_cost =  AffinityCost(worker_graph, x_task, y_task, data_task_network[x][y])

                    if x_task and y_task and associated_affinity_cost:
                        task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)

        print("Task Graph setup successful")


    # Evaluate using Brute Force Scheduling Algorithm
    print("\n--- Brute Force Scheduling Algorithm ---")
    start_time = time.time()  # Record the start time

    bf = BruteForce(workers, tasks, worker_graph, task_graph)
    perms, deps, min_netcost = bf.run()

    sched_algo_log_helper(len(workers), len(tasks), perms, deps, min_netcost)     

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken: {elapsed_time} seconds\n")
