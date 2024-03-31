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

    # Load, Validate & Construct Workers
    with open((os.path.join("in/workers", f"workers.json")), 'r') as file:
        data = json.load(file)

        for entry in data:
            workers.append(Worker(id=entry["id"], cpu=entry["cpu"], memory=entry["memory"], disk=entry["disk"]))

        print("Workers loading successful")

    # Load, Validate & Construct Links
    with open((os.path.join("in/links", f"links.json")), 'r') as file:
        data = json.load(file)

        for entry in data:
            links.append(Link(id=entry["id"], response_time=entry["response_time"]))

        print("Links loading successful")

    # Load, Validate & Construct Worker Network
    with open((os.path.join("in/worker_network", f"worker_network.json")), 'r') as file:
        data = json.load(file)

        data_used_workers=data["used_workers"]
        data_used_links=data["used_links"]
        data_worker_graph=data["worker_graph"]

        for x in range(0, len(data_used_workers)):
            for y in range(0, len(data_used_workers)):
                # Find Workers
                x_worker = find_worker(workers, data_used_workers[x])
                y_worker = find_worker(workers, data_used_workers[y])

                # Find Links
                associated_link = find_link(links, data_worker_graph[x][y])

                if x_worker and y_worker and associated_link:
                    worker_graph.add_link(x_worker, y_worker, associated_link)

        print("Worker Graph setup successful")

    # Load, Validate & Construct Tasks
    with open((os.path.join("in/tasks", f"tasks.json")), 'r') as file:
        data = json.load(file)

        for entry in data:
            tasks.append(Task(id=entry["id"], cpu_required=entry["cpu_required"], memory_required=entry["memory_required"], disk_required=entry["disk_required"]))

        print("Task loading successful")

    # Load, Validate & Construct Deployments
    with open((os.path.join("in/deps", f"deps.json")), 'r') as file:
        data = json.load(file)
        
        for key, values in data.items():
            deploying_worker = find_worker(workers, key)
            for value in values:
                task_to_be_deployed = find_task(tasks, value)
                deploying_worker.deploy_task(task_to_be_deployed)

        print("Deployment successful")

    
    # Load, Validate & Construct Task Network
    with open((os.path.join("in/task_network", f"task_network.json")), 'r') as file:
        data = json.load(file)

        data_used_tasks=data["used_tasks"]
        data_task_graph=data["task_graph"]

        for x in range(0, len(data_used_tasks)):
            for y in range(0, len(data_used_tasks)):
                if x != y:
                    # Find Tasks
                    x_task = find_task(tasks, data_used_tasks[x])
                    y_task = find_task(tasks, data_used_tasks[y])

                    # Find Affinity Cost
                    associated_affinity_cost =  AffinityCost(worker_graph, x_task, y_task, data_task_graph[x][y])

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
