import json
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from utils.plotter import Plotter

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    sim_result_to_plot = f"logs_2024-04-11_00-14-05"

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
        bf_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BF NetCost"]) for entry in data]
        bp_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BP NetCost"]) for entry in data]
        bf_netcost = [entry["BF NetCost"] for entry in data]
        bp_netcost = [entry["BP NetCost"] for entry in data]

        # Plotting first figure: Worker & Task vs Simulation Count
        bf_worker_task_netcost_plot = Plotter(range(len(bf_worker_task_netcost)), bf_netcost, 'BruteForce: (Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost' )
        bp_worker_task_netcost_plot = Plotter(range(len(bp_worker_task_netcost)), bp_netcost, 'BinPack: (Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        
        bf_worker_task_netcost_plot.plot(xticks=workers_tasks, color='red')
        bp_worker_task_netcost_plot.plot(xticks=workers_tasks, color='blue')

        # Save the first plot as image
        bf_worker_task_netcost_plot.save_plot(os.path.join(figures_folder, f"bf_worker_task_netcost.png"), xticks=workers_tasks, color='red')
        bp_worker_task_netcost_plot.save_plot(os.path.join(figures_folder, f"bp_worker_task_netcost.png"), xticks=workers_tasks, color='blue')

        # Extracting worker, task, and time taken
        bf_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BF Computation Time"]) for entry in data]
        bp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BP Computation Time"]) for entry in data]
        bf_time_taken = [entry["BF Computation Time"] for entry in data]
        bp_time_taken = [entry["BP Computation Time"] for entry in data]

        # Plotting second figure: Worker & Task vs Time Taken
        bf_worker_task_sim_counts_plot = Plotter(range(len(bf_worker_task_time)), bf_time_taken, 'BruteForce: (Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        bp_worker_task_sim_counts_plot = Plotter(range(len(bp_worker_task_time)), bp_time_taken, 'BinPack: (Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        
        bf_worker_task_sim_counts_plot.plot(xticks=workers_tasks, color='red')
        bp_worker_task_sim_counts_plot.plot(xticks=workers_tasks, color='blue')

        # Save the second plot as image
        bf_worker_task_sim_counts_plot.save_plot(os.path.join(figures_folder, f"bf_worker_task_time_taken.png"), xticks=workers_tasks, color='red')
        bp_worker_task_sim_counts_plot.save_plot(os.path.join(figures_folder, f"bp_worker_task_time_taken.png"), xticks=workers_tasks, color='blue')