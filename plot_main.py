import json
import os
from dotenv import load_dotenv

from utils.plot.multi_plot import MultiPlotter

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    sim_result_to_plot = os.getenv("TARGET_LOG")

    print(sim_result_to_plot)

    # Read data from JSON file
    with open((os.path.join("out/sim_results", f"{sim_result_to_plot}.json")), 'r') as file:
        data = json.load(file)

        # Create a new folder for figures if it doesn't exist
        figures_folder = os.path.join("out/figs", sim_result_to_plot)
        if not os.path.exists(figures_folder):
            os.makedirs(figures_folder)

        # Extracting worker, task, and simulation count
        workers_tasks = [(entry["Workers"], entry["Tasks"]) for entry in data]
        # bf_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BF NetCost"]) for entry in data]
        bp_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BP NetCost"]) for entry in data]
        m3c_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["M3C NetCost"]) for entry in data]
        # bf_netcost = [entry["BF NetCost"] for entry in data]
        bp_netcost = [entry["BP NetCost"] for entry in data]
        m3c_netcost = [entry["M3C NetCost"] for entry in data]

        plt1 = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        # plt1.plot(range(len(bf_worker_task_netcost)), bf_netcost, "Brute Force")
        plt1.plot(range(len(bp_worker_task_netcost)), bp_netcost, "Bin Pack")
        plt1.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "M3C")
        plt1.show()

        plt1.save(os.path.join(figures_folder, f"worker_task_netcost.png"))


        # Extracting worker, task, and time taken
        # bf_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BF Computation Time"]) for entry in data]
        bp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BP Computation Time"]) for entry in data]
        m3c_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["M3C Computation Time"]) for entry in data]
        # bf_time_taken = [entry["BF Computation Time"] for entry in data]
        bp_time_taken = [entry["BP Computation Time"] for entry in data]
        m3c_time_taken = [entry["M3C Computation Time"] for entry in data]
        

        plt2 = MultiPlotter('(Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        # plt2.plot(range(len(bf_worker_task_time)), bf_time_taken, "Brute Force")
        plt2.plot(range(len(bp_worker_task_time)), bp_time_taken, "Bin Pack")
        plt2.plot(range(len(m3c_worker_task_time)), m3c_time_taken, "M3C")
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_computation_time.png"))