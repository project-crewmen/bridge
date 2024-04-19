import os
import json
import time
from dotenv import load_dotenv

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_affinity_graph import TaskAffinityGraph

from utils.crewmen_utils import load_all
from utils.console_log_utils import print_sched_algo_results

from scheduling_algorithms.bin_pack.bin_pack import BinPack

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Access environment variables
    log_dir_name = os.getenv("SINGLE_TARGET_LOG")  
    
    with open((os.path.join("in", f"{log_dir_name}.json")), 'r') as file:
        workers: list[Worker] = []
        links: list[Link] = []
        worker_graph = WorkerGraph()
        tasks: list[Task] = []
        task_affinity_graph = TaskAffinityGraph()

        data = json.load(file)

        # Load All
        load_all(data, workers, links, worker_graph, tasks, task_affinity_graph)

        # Evaluate Binpack Scheduling Algorithm
        start_time = time.time()
        bp = BinPack(workers, tasks, worker_graph, task_affinity_graph)
        binpacked_deployment, net_cost, total_colocations = bp.run()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_sched_algo_results("Binpack Scheduling Algorithm", net_cost, total_colocations, elapsed_time)
