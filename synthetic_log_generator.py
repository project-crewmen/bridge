import os
import json
import random

from utils.time import get_human_readable_timestamp
from utils.crewmen_utils import find_worker, find_link, find_task

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.globaldeployment import GlobalDeployment
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.communication import Communication
from crewmen.crewmen import Crewmen

# Worker Configurations
WORKER_CONFIG_CPU_RANGE=(4,8)
WORKER_CONFIG_MEMORY_RANGE=(1024*5, 1024*5*4)
WORKER_CONFIG_DISK_RANGE=(4096*10, 4096*10*4)

# Link Configurations
LINK_CONFIG_RESPONSE_TIME_RANGE=(0, 1)

# Task Configurations
TASK_CONFIG_CPU_REQUIRED_RANGE=(1,1)
TASK_CONFIG_MEMORY_REQUIRED_RANGE=(512, 1024*4)
TASK_CONFIG_DISK_REQUIRED_RANGE=(1024*2, 1024*10)

# Task Affinity Configurations
TASK_AFFINITY_CONFIG_MESSAGE_PASSED_RANGE=(10*10, 1000*10)
TASK_AFFINITY_CONFIG_DATA_EXCHANGED_RANGE=(1024*4, 1024*4*10)


if __name__ == "__main__":
    # Create a new folder for logs if it doesn't exist
    human_readable_time = get_human_readable_timestamp()
    folder_name = f"logs_{human_readable_time}"
    logs_folder = os.path.join("in/", folder_name)
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    wm = Crewmen()

    for x in range(3, 23):
        file_name =  f"{x}_log"

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
                worker: Worker = Worker(id=f"w_{w}", cpu=random.randint(*WORKER_CONFIG_CPU_RANGE), memory=random.randint(*WORKER_CONFIG_MEMORY_RANGE), disk=random.randint(*WORKER_CONFIG_DISK_RANGE))
                workers.append(worker)

            # Generate Links
            # Number of Links Required
            # Since Worker Graph is a FullyConnectedGraph, for n nodes, there exists (n(n-1))/2 edges
            l_amt = (w_amt * (w_amt-1))//2
            links.append(Link(id=f"l_{0}", response_time = 0.0000))
            for l in range(1, l_amt+1):
                link: Link = Link(id=f"l_{l}", response_time=round(random.uniform(*LINK_CONFIG_RESPONSE_TIME_RANGE), 4))
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
                task: Task = Task(id=f"t_{t}", cpu_required=random.randint(*TASK_CONFIG_CPU_REQUIRED_RANGE), memory_required=random.randint(*TASK_CONFIG_MEMORY_REQUIRED_RANGE), disk_required=random.randint(*TASK_CONFIG_DISK_REQUIRED_RANGE))
                tasks.append(task)

            # Generate Deployment: Using Spread Strategy
            randomized_tasks = random.sample(tasks, len(tasks))

            for w in range(0, w_amt):
                deploying_worker = find_worker(workers, f"w_{w}")
                task_to_be_deployed = randomized_tasks[w]
                deploying_worker.deploy_task(task_to_be_deployed)

                deployments.record_deployment(deploying_worker.id, task_to_be_deployed.id)

            # print(deployments)

            # Message passed and Data echanged generation for each task pair
            communications: list[Communication] = []

            for i in range(0, t_amt):
                for j in range(i, t_amt):
                    if i != j:
                        msg_passed = random.randint(*TASK_AFFINITY_CONFIG_DATA_EXCHANGED_RANGE)
                        data_exchanged = random.randint(*TASK_AFFINITY_CONFIG_DATA_EXCHANGED_RANGE)

                        communications.append(Communication(f"t_{i}", f"t_{j}", msg_passed, data_exchanged))

            total_message_passed_amt = 0
            total_data_exchanged_amt = 0

            for com in communications:
                total_message_passed_amt += com.message_passed
                total_data_exchanged_amt += com.data_exchanged

            for com in communications:
                x_task = find_task(tasks, com.x_task)
                y_task = find_task(tasks, com.y_task)

                if x_task and y_task:
                    task_affinity_graph.add_affinity(x_task, y_task, wm.affinity(total_message_passed_amt, total_data_exchanged_amt, com.message_passed, com.data_exchanged))


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