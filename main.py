import os
import gc
import json
import time
import re
from dotenv import load_dotenv

from crewmen.worker import Worker
from crewmen.link import Link
from crewmen.worker_graph import WorkerGraph
from crewmen.task import Task
from crewmen.task_affinity_graph import TaskAffinityGraph

from utils.crewmen_utils import load_all, load_deployments

from scheduling_algorithms.bf.bf import BruteForce
from scheduling_algorithms.bin_pack.bin_pack import BinPack
from scheduling_algorithms.m3c.m3c import M3C

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
                # filepath = os.path.join("in", log_dir_name, filename)
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

                    # # Evaluate using Brute Force Scheduling Algorithm
                    # print("\n--- Brute Force Scheduling Algorithm ---")
                    # start_time = time.time()  # Record the start time

                    # bf = BruteForce(workers, tasks, worker_graph, task_affinity_graph)
                    # perms, deps, min_netcost = bf.run()

                    # # sched_algo_log_helper(len(workers), len(tasks), perms, deps, min_netcost)
                    # print("Netcost: ", min_netcost)     

                    # end_time = time.time()  # Record the end time
                    # bf_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    # print(f"Time taken: {bf_elapsed_time} seconds\n")


                    # Reset Deployment
                    for w in workers:
                        w.clear_deployments()

                    load_deployments(data, workers, tasks)


                    # Evaluate using Binpack Force Scheduling Algorithm
                    print("\n--- Binpack Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    bp = BinPack(workers, tasks, worker_graph, task_affinity_graph)
                    binpacked_deployment, net_cost = bp.run()

                    # sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, net_cost)   
                    print("Netcost: ", net_cost)       

                    end_time = time.time()  # Record the end time
                    bp_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {bp_elapsed_time} seconds\n")



                    # Evaluate using M3C Force Scheduling Algorithm
                    print("\n--- Binpack Scheduling Algorithm ---")
                    start_time = time.time()  # Record the start time

                    m3c = M3C(workers, tasks, worker_graph, task_affinity_graph)
                    m3c_deployment, m3c_net_cost = m3c.run()

                    # sched_algo_log_helper(len(workers), len(tasks), binpacked_deployment, net_cost)   
                    print("Netcost: ", m3c_net_cost)       

                    end_time = time.time()  # Record the end time
                    m3c_elapsed_time = end_time - start_time  # Calculate the elapsed time
                    print(f"Time taken: {m3c_elapsed_time} seconds\n")

                    # Output to a JSON file
                    # Create a dictionary with the test results
                    test_result = {
                        "Test": t,
                        "Workers": len(workers),
                        "Tasks": len(tasks),
                        # "BF NetCost": min_netcost,
                        # "BF Computation Time": bf_elapsed_time,
                        "BP NetCost": net_cost,
                        "BP Computation Time": bp_elapsed_time,
                        "M3C NetCost": m3c_net_cost,
                        "M3C Computation Time": m3c_elapsed_time,
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
