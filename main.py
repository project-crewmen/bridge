import os
import json

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task

def find_worker(workers: list[Worker], id: str):
    return next((worker for worker in workers if worker.id == id), None)

def find_link(links: list[Link], id: str):
    return next((link for link in links if link.id == id), None)

def find_task(tasks: list[Task], id: str):
    return next((task for task in tasks if task.id == id), None)

if __name__ == "__main__":
    workers: list[Worker] = []
    links: list[Link] = []
    worker_graph = WorkerGraph()
    tasks: list[Task] = []

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
