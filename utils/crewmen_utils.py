from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
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