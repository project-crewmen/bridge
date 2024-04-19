import os
import gc
import json
import time
import re
from dotenv import load_dotenv

from crewmen.crewmen import Crewmen
from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import load_all, load_deployments
from utils.crewmen_utils import  find_task
from utils.graph_visualization.graph_visializer import GraphVisulizer
from utils.console_log_utils import print_sched_algo_results

from scheduling_algorithms.bf.bf import BruteForce
from scheduling_algorithms.bin_pack.bin_pack import BinPack
from scheduling_algorithms.e_pvm.e_pvm import EPVM
from scheduling_algorithms.kube_scheduler.kube_scheduler import KubeScheduler
from scheduling_algorithms.m3c.m3c import M3C

def alphanumeric_sort_key(filename):
    # Extract the numeric part of the filename using regular expression
    numeric_part = re.search(r'\d+', filename)
    if numeric_part:
        numeric_part = int(numeric_part.group())
    else:
        numeric_part = float('inf')  # Set a very large number if no numeric part found
    return (numeric_part, filename)  # Sort first by numeric part, then by entire filename

def reset_deployments(data, workers: list[Worker], tasks: list[Task]):
    # Clear the exisitng deployment
    for w in workers:
        w.clear_deployments()

    # Reload the deployments
    load_deployments(data, workers, tasks)

# Main Function
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Access environment variables
    log_dir_name = os.getenv("TARGET_LOG")    

    with open((os.path.join("out/sim_results", f"{log_dir_name}.json")), "w") as results_file:
        results_file.write("[\n")

        t = 1
        sorted_filenames: list[str] = []
        for filename in os.listdir(os.path.join("in", log_dir_name)):
            if filename.endswith(".json"):  # Check for JSON files only
                sorted_filenames.append(filename)

        sorted_filenames = sorted(sorted_filenames, key=alphanumeric_sort_key)

        for idx, filename in enumerate(sorted_filenames):
                workers: list[Worker] = []
                links: list[Link] = []
                worker_graph = WorkerGraph()
                tasks: list[Task] = []
                task_affinity_graph = TaskAffinityGraph()
                
                with open((os.path.join("in", log_dir_name, filename)), 'r') as file:
                    data = json.load(file)

                    # Load All
                    load_all(data, workers, links, worker_graph, tasks, task_affinity_graph)
                    print(f"\nWorkers: {len(workers)} | Tasks: {len(tasks)}")

                    # Base Setup
                    wm = Crewmen()

                    # Save previous deployment
                    previous_deployment = GlobalDeployment(f"previous_deployment")

                    for w in workers:
                        t_ids = w.get_deployment_ids()
                        for tid in t_ids:
                                previous_deployment.record_deployment(w.id, tid)

                    # Constructing Task Graph (Node: Task, Edge: Affinity)
                    task_graph = TaskGraph()
                    task_graph.initialize(tasks, worker_graph, task_affinity_graph) 

                    # print(task_graph)
                    # gv1 = GraphVisulizer(task_graph.network.graph)
                    # gv1.show()

                    # Net Cost
                    initial_net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
                    # print(initial_net_cost)                         



                    """
                    WARNING !!!- UNABLE BRUTE FORCE ALGORITHM ONLY WHEN REQUIRED - TIME COMPLEXITY IS EXPONENTIAL
                    """
                    # """
                    # Evaluate using Brute Force Scheduling Algorithm
                    # """
                    # # Reset Deployment
                    # reset_deployments(data, workers, tasks)
                    # # Execute Timer & Evaluate
                    # start_time = time.time()
                    # bf = BruteForce(workers, tasks, worker_graph, task_affinity_graph)
                    # perms, deps, bf_net_cost, bf_total_colocations = bf.run()
                    # end_time = time.time()
                    # bf_elapsed_time = end_time - start_time
                    # print_sched_algo_results("Brute Force Scheduling Algorithm", bf_net_cost, bf_total_colocations, bf_elapsed_time)



                    """
                    Evaluate Binpack Scheduling Algorithm
                    """
                    # Reset Deployment
                    reset_deployments(data, workers, tasks)
                    # Execute Timer & Evaluate
                    start_time = time.time() 
                    bp = BinPack(workers, tasks, worker_graph, task_affinity_graph)
                    binpacked_deployment, bp_net_cost, bp_total_colocations = bp.run() 
                    end_time = time.time()
                    bp_elapsed_time = end_time - start_time
                    print_sched_algo_results("Binpack Scheduling Algorithm", bp_net_cost, bp_total_colocations, bp_elapsed_time)



                    """
                    Evaluate EPVM Scheduling Algorithm
                    """
                    # Reset Deployment
                    reset_deployments(data, workers, tasks)
                    # Execute Timer & Evaluate
                    start_time = time.time()
                    epvm = EPVM(workers, tasks, worker_graph, task_affinity_graph)
                    epvm_deployment, epvm_net_cost, epvm_total_colocations = epvm.run()
                    end_time = time.time()
                    epvm_elapsed_time = end_time - start_time 
                    print_sched_algo_results("EPVM Scheduling Algorithm", epvm_net_cost, epvm_total_colocations, epvm_elapsed_time)



                    """
                    Evaluate KubeScheduler Scheduling Algorithm
                    """
                    # Reset Deployment
                    reset_deployments(data, workers, tasks)
                    # Execute Timer & Evaluate
                    start_time = time.time()
                    kube_sched = KubeScheduler(workers, tasks, worker_graph, task_affinity_graph)
                    kube_sched_deployment, kube_sched_net_cost, kube_sched_total_colocations = kube_sched.run()
                    end_time = time.time()
                    kube_sched_elapsed_time = end_time - start_time
                    print_sched_algo_results("KubeScheduler Scheduling Algorithm", kube_sched_net_cost, kube_sched_total_colocations, kube_sched_elapsed_time)



                    """
                    Evaluate M3C Scheduling Algorithm
                    """
                    # Reset Deployment
                    reset_deployments(data, workers, tasks)
                    # Execute Timer & Evaluate
                    start_time = time.time()
                    m3c = M3C(workers, tasks, worker_graph, task_affinity_graph)
                    m3c_deployment, m3c_net_cost, m3c_total_colocations = m3c.run()
                    end_time = time.time() 
                    m3c_elapsed_time = end_time - start_time 
                    print_sched_algo_results("M3C Scheduling Algorithm", m3c_net_cost, m3c_total_colocations, m3c_elapsed_time)

                    # Output to a JSON file
                    # Create a dictionary with the test results
                    test_result = {
                        "Test": t,
                        "Workers": len(workers),
                        "Tasks": len(tasks),
                        "Initial NetCost": initial_net_cost,
                        # "BF NetCost": bf_net_cost,
                        # "BF Computation Time": bf_elapsed_time,
                        # "BF Total Colocations": bf_total_colocations,
                        "BP NetCost": bp_net_cost,
                        "BP Computation Time": bp_elapsed_time,
                        "BP Total Colocations": bp_total_colocations,
                        "EPVM NetCost": epvm_net_cost,
                        "EPVM Computation Time": epvm_elapsed_time,
                        "EPVM Total Colocations": epvm_total_colocations,
                        "KubeScheduler NetCost": kube_sched_net_cost,
                        "KubeScheduler Computation Time": kube_sched_elapsed_time,
                        "KubeScheduler Total Colocations": kube_sched_total_colocations,
                        "M3C NetCost": m3c_net_cost,
                        "M3C Computation Time": m3c_elapsed_time,
                        "M3C Total Colocations": m3c_total_colocations,
                    }

                    # Convert the dictionary to a JSON string
                    json_string = json.dumps(test_result)

                    # Write the JSON string to the file
                    results_file.write(json_string)
                    # Add comma and newline if it's not the last file
                    if idx < len(sorted_filenames) - 1:
                        results_file.write(",\n")
                    else:
                        results_file.write("\n")

                    results_file.flush()

                    t += 1 

        # Clean up memory
        gc.collect()
    
        results_file.write("]\n")
