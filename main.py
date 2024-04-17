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

from scheduling_algorithms.bf.bf import BruteForce
from scheduling_algorithms.bin_pack.bin_pack import BinPack
# from scheduling_algorithms.extended_bin_pack.extended_bin_pack import ExtendedBinPack
from scheduling_algorithms.e_pvm.e_pvm import EPVM
from scheduling_algorithms.kube_scheduler.kube_scheduler import KubeScheduler
from scheduling_algorithms.m3c.m3c import M3C

def sched_algo_log_helper(w_amt, t_amt, perms, deps, bf_net_cost):
    print(f"--- Test #{1} - Workers: {w_amt} | Tasks: {t_amt} ---")
    print(f"Total number of permutations:\t\t{perms}")
    print(f"Deployement Set (Least Net Cost):\t{len(deps)}")
    # dep_maps: list[str] = []
    # # print(deps)
    # for d in deps:
    #     dep_maps.append(d.get_display_text())

    # print(dep_maps)

    print("Minimum Netcost: ", bf_net_cost, "\n")


def alphanumeric_sort_key(filename):
    # Extract the numeric part of the filename using regular expression
    numeric_part = re.search(r'\d+', filename)
    if numeric_part:
        numeric_part = int(numeric_part.group())
    else:
        numeric_part = float('inf')  # Set a very large number if no numeric part found
    return (numeric_part, filename)  # Sort first by numeric part, then by entire filename


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

        for filename in sorted_filenames:
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

                    for i in range(0, len(tasks)):
                        for j in range(i, len(tasks)):
                                if i != j:
                                    # Find Tasks
                                    x_task = find_task(tasks, f"t_{i}")
                                    y_task = find_task(tasks, f"t_{j}")

                                    # Find Affinity Cost
                                    associated_affinity_cost =  AffinityCost(worker_graph, x_task, y_task, task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                                    if x_task and y_task and associated_affinity_cost:
                                        task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)       


                    # print(task_graph)

                    # gv1 = GraphVisulizer(task_graph.network.graph)
                    # gv1.show()

                    # Net Cost
                    initial_net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
                    # print(initial_net_cost)                         

                    # # Evaluate using Brute Force Scheduling Algorithm
                    # print("\n--- Brute Force Scheduling Algorithm ---")
                    # start_time = time.time()  # Record the start time

                    # bf = BruteForce(workers, tasks, worker_graph, task_affinity_graph)
                    # perms, deps, bf_net_cost, bf_total_colocations = bf.run()

                    # # sched_algo_log_helper(len(workers), len(tasks), perms, deps, bf_net_cost)
                    # print("Netcost: ", bf_net_cost)     
                    # print("Total Colocations: ", bf_total_colocations)     

                    # end_time = time.time()  # Record the end time
                    # bf_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    # print(f"Time taken: {bf_elapsed_time} seconds\n")


                    # Reset Deployment
                    for w in workers:
                        w.clear_deployments()

                    load_deployments(data, workers, tasks)




                    # Evaluate using Binpack Scheduling Algorithm
                    print("\n--- Binpack Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    bp = BinPack(workers, tasks, worker_graph, task_affinity_graph)
                    binpacked_deployment, bp_net_cost, bp_total_colocations = bp.run()

                    # sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, bp_net_cost)   
                    print("Netcost: ", bp_net_cost)    
                    print("Total Colocations: ", bp_total_colocations)      

                    end_time = time.time()  # Record the end time
                    bp_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {bp_elapsed_time} seconds\n")


                    # # Reset Deployment
                    # for w in workers:
                    #     w.clear_deployments()

                    # load_deployments(data, workers, tasks)




                    # # Evaluate using ExtendedBinPack Scheduling Algorithm
                    # print("\n--- ExtendedBinPack Scheduling Algorithm ---")
                    # start_time = time.time()  # Record the start time

                    # ebp = ExtendedBinPack(workers, tasks, worker_graph, task_affinity_graph)
                    # binpacked_deployment, ebp_net_cost, ebp_total_colocations = ebp.run()

                    # # sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, ebp_net_cost)   
                    # print("Netcost: ", ebp_net_cost)    
                    # print("Total Colocations: ", ebp_total_colocations)      

                    # end_time = time.time()  # Record the end time
                    # ebp_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    # print(f"Time taken: {ebp_elapsed_time} seconds\n")


                    


                    # Reset Deployment
                    for w in workers:
                        w.clear_deployments()

                    load_deployments(data, workers, tasks)



                    # Evaluate using EPVM Scheduling Algorithm
                    print("\n--- EPVM Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    epvm = EPVM(workers, tasks, worker_graph, task_affinity_graph)
                    epvm_deployment, epvm_net_cost, epvm_total_colocations = epvm.run()

                    # sched_algo_log_helper(len(workers), len(tasks), epvm_deployment, epvm_net_cost)   
                    print("Netcost: ", epvm_net_cost)    
                    print("Total Colocations: ", epvm_total_colocations)      

                    end_time = time.time()  # Record the end time
                    epvm_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {epvm_elapsed_time} seconds\n")


                    # Reset Deployment
                    for w in workers:
                        w.clear_deployments()

                    load_deployments(data, workers, tasks)



                    # Evaluate using KubeScheduler Scheduling Algorithm
                    print("\n--- KubeScheduler Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    kube_sched = KubeScheduler(workers, tasks, worker_graph, task_affinity_graph)
                    kube_sched_deployment, kube_sched_net_cost, kube_sched_total_colocations = kube_sched.run()

                    # sched_algo_log_helper(len(workers), len(tasks), kube_sched_deployment, kube_sched_net_cost)   
                    print("Netcost: ", kube_sched_net_cost)    
                    print("Total Colocations: ", kube_sched_total_colocations)      

                    end_time = time.time()  # Record the end time
                    kube_sched_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {kube_sched_elapsed_time} seconds\n")




                    # Reset Deployment
                    for w in workers:
                        w.clear_deployments()

                    load_deployments(data, workers, tasks)




                    # Evaluate using M3C Scheduling Algorithm
                    print("\n--- M3C Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    m3c = M3C(workers, tasks, worker_graph, task_affinity_graph)
                    m3c_deployment, m3c_net_cost, m3c_total_colocations = m3c.run()

                    # sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, net_cost)   
                    print("Netcost: ", m3c_net_cost)        
                    print("Total Colocations: ", m3c_total_colocations)       

                    end_time = time.time()  # Record the end time
                    m3c_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {m3c_elapsed_time} seconds\n")

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
                        # "EBP NetCost": ebp_net_cost,
                        # "EBP Computation Time": ebp_elapsed_time,
                        # "EBP Total Colocations": ebp_total_colocations,
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
                    results_file.write(json_string + ",\n")
                    results_file.flush()

                    t += 1 

        # Clean up memory
        gc.collect()
    
        results_file.write("]\n")
