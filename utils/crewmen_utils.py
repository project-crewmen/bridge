from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen

# ID Filters
def get_worker_ids(workers: list[Worker]):
    ids: list[str] = []
    for w in workers:
        ids.append(w.id)

    return ids

def get_link_ids(links: list[Link]):
    ids: list[str] = []
    for l in links:
        ids.append(l.id)

    return ids

def get_task_ids(tasks: list[Task]):
    ids: list[str] = []
    for t in tasks:
        ids.append(t.id)

    return ids


# Finders 
def find_worker(workers: list[Worker], id: str):
    return next((worker for worker in workers if worker.id == id), None)

def find_link(links: list[Link], id: str):
    return next((link for link in links if link.id == id), None)

def find_task(tasks: list[Task], id: str):
    return next((task for task in tasks if task.id == id), None)


# JSON Parsers & Loader
def load_workers(data, workers: list[Worker]):
    data_workers=data["workers"]

    for entry in data_workers:
        workers.append(Worker(id=entry["id"], cpu=entry["cpu"], memory=entry["memory"], disk=entry["disk"]))

    # print("Workers loading successful")

def load_links(data, links: list[Link]):
    data_links=data["links"]

    for entry in data_links:
        links.append(Link(id=entry["id"], response_time=entry["response_time"]))

    # print("Links loading successful")

def load_worker_graph(data, worker_graph: WorkerGraph, workers: list[Worker], links: list[Link]):
    data_workers=data["workers"]
    data_worker_network=data["worker_graph"]

    k = 1
    for i in range(0, len(data_workers)):
        for j in range(i, len(data_workers)):
            if i == j:
                worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{0}"))
            else:
                worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{k}"))
                k += 1

    # print("Worker Graph setup successful")

def load_tasks(data, tasks: list[Task]):
    data_tasks=data["tasks"]

    for entry in data_tasks:
        tasks.append(Task(id=entry["id"], cpu_required=entry["cpu_required"], memory_required=entry["memory_required"], disk_required=entry["disk_required"]))

    # print("Task loading successful")

def load_deployments(data, workers: list[Worker], tasks: list[Task]):
    data_deployments=data["deployments"]
        
    for key, values in data_deployments.items():
        deploying_worker = find_worker(workers, key)
        for value in values:
            task_to_be_deployed = find_task(tasks, value)
            deploying_worker.deploy_task(task_to_be_deployed)

    # print("Deployment successful")

def load_task_affinity_graph(data, tasks: list[Task], task_affinity_graph: TaskAffinityGraph):
    data_tasks=data["tasks"]
    data_task_affinity_graph=data["task_affinity_graph"]

    for i in range(0, len(data_tasks)):
        for j in range(i, len(data_tasks)):
            if i != j:
                # Find Tasks
                x_task = find_task(tasks, f"t_{i}")
                y_task = find_task(tasks, f"t_{j}")

                if x_task and y_task:
                    task_affinity_graph.add_affinity(x_task, y_task, data_task_affinity_graph[i][j])

    # print("Task Affinity Graph setup successful")
    # print(task_affinity_graph)

def load_all(data, workers: list[Worker], links: list[Link], worker_graph: WorkerGraph, tasks: list[Task], task_affinity_graph: TaskAffinityGraph):
    # Load, Validate & Construct Workers
    load_workers(data, workers)

    # Load, Validate & Construct Links
    load_links(data, links)

    # Load, Validate & Construct Worker Network
    load_worker_graph(data, worker_graph, workers, links)

    # Load, Validate & Construct Tasks
    load_tasks(data, tasks)

    # Load, Validate & Construct Deployments
    load_deployments(data, workers, tasks)

    # Load, Validate & Construct Task Affinity Network
    load_task_affinity_graph(data, tasks, task_affinity_graph)