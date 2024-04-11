import gc
import time
import os
import json
import random
from dotenv import load_dotenv

from utils.time import get_human_readable_timestamp
from utils.crewmen_utils import find_worker, find_link, find_task

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.globaldeployment import GlobalDeployment
from crewmen.task_affinity_graph import TaskAffinityGraph


if __name__ == "__main__":
    # Create a new folder for logs if it doesn't exist
    human_readable_time = get_human_readable_timestamp()
    folder_name = f"logs_{human_readable_time}"
    logs_folder = os.path.join("in/", folder_name)
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    for x in range(3, 11):
        file_name =  f"log_{x}_w_{x}_t{x}"

        with open((os.path.join(f"in/{folder_name}", f"{file_name}.json")), "a") as results_file:
            workers: list[Worker] = []
            links: list[Link] = []
            tasks: list[Task] = []
            worker_graph = WorkerGraph()
            deployments = GlobalDeployment()
            task_affinity_graph = TaskAffinityGraph()

            # Generate Workers
            w_amt: int = x
            for w in range(0, w_amt):
                worker: Worker = Worker(id=f"w_{w}")
                workers.append(worker)

            # Generate Links
            # Number of Links Required
            # Since Worker Graph is a FullyConnectedGraph, for n nodes, there exists (n(n-1))/2 edges
            l_amt = (w_amt * (w_amt-1))//2
            links.append(Link(id=f"l_{0}", response_time = 0.0000))
            for l in range(1, l_amt+1):
                link: Link = Link(id=f"l_{l}", response_time=round(random.uniform(0, 1), 4))
                links.append(link)

            # Constructing Fully Connected Worker Graph (Node: Worker, Edge: Link)
            k = 1
            for i in range(0, w_amt):
                for j in range(i, w_amt):
                    if i == j:
                        worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{0}"))
                    else:
                        worker_graph.add_link(find_worker(workers, f"w_{i}"), find_worker(workers, f"w_{j}"), find_link(links, f"l_{k}"))
                        k += 1

            # Generate Tasks
            t_amt: int = x
            for t in range(0, t_amt):
                task: Task = Task(id=f"t_{t}")
                tasks.append(task)

            # Generate Deployment
            for w in range(0, w_amt):
                deploying_worker = find_worker(workers, f"w_{w}")
                task_to_be_deployed = find_task(tasks, f"t_{w}")
                deploying_worker.deploy_task(task_to_be_deployed)

                deployments.record_deployment(deploying_worker.id, task_to_be_deployed.id)

            # Construct Task Affinity Cost Graph
            for i in range(0, t_amt):
                for j in range(i, t_amt):
                    if i != j:
                        # Find Tasks
                        x_task = find_task(tasks, f"t_{i}")
                        y_task = find_task(tasks, f"t_{j}")

                        if x_task and y_task:
                            task_affinity_graph.add_affinity(x_task, y_task, round(random.uniform(0, 1), 4))


            # Spec parse
            worker_specs = [w.get_worker_spec() for w in workers]
            link_specs = [l.get_link_spec() for l in links]
            task_specs = [t.get_task_spec() for t in tasks]
            worker_graph_spec = worker_graph.get_worker_graph_spec()
            deployment_spec = deployments.get_global_deployment_spec()
            task_affinity_graph_spec = task_affinity_graph.get_task_affinity_graph_spec()
                
            schema = {
                "workers": worker_specs,
                "links": link_specs,
                "worker_graph": worker_graph_spec,
                "tasks": task_specs,
                "deployments": deployment_spec,
                "task_affinity_graph": task_affinity_graph_spec,
            }

            # Convert the dictionary to a JSON string
            json_string = json.dumps(schema)

            # Write the JSON string to the file
            results_file.write(json_string)
            results_file.flush()

            results_file.close()