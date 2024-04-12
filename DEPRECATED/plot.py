import json
import os
from dotenv import load_dotenv

from utils.plot.plotter import Plotter

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    sim_result_to_plot = os.getenv("SIM_RESULT_TO_PLOT")

    print(sim_result_to_plot)

    # Read data from JSON file
    with open((os.path.join("out/sim_results", f"{sim_result_to_plot}.json")), 'r') as file:
        data = json.load(file)

        # Create a new folder for figures if it doesn't exist
        figures_folder = os.path.join("out/figs", sim_result_to_plot)
        if not os.path.exists(figures_folder):
            os.makedirs(figures_folder)

        # Extracting worker, task, and simulation count
        worker_task_simulations = [(entry["Workers"], entry["Tasks"], entry["Total number of permutations"]) for entry in data]
        workers_tasks = [(entry["Workers"], entry["Tasks"]) for entry in data]
        simulations = [entry["Total number of permutations"] for entry in data]

        # Plotting first figure: Worker & Task vs Simulation Count
        worker_task_sim_counts_plot = Plotter(range(len(worker_task_simulations)), simulations, '(Worker, Task) vs Simulation Count', '(Worker, Task)', 'Simulation Count')
        worker_task_sim_counts_plot.plot(xticks=workers_tasks)

        # Save the first plot as image
        worker_task_sim_counts_plot.save_plot(os.path.join(figures_folder, f"worker_task_simulation_count.png"), xticks=workers_tasks)

        # Extracting worker, task, and time taken
        worker_task_time = [(entry["Workers"], entry["Tasks"], entry["Time_taken"]) for entry in data]
        time_taken = [entry["Time_taken"] for entry in data]

        # Plotting second figure: Worker & Task vs Time Taken
        worker_task_sim_counts_plot = Plotter(range(len(worker_task_time)), time_taken, '(Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        worker_task_sim_counts_plot.plot(xticks=workers_tasks, color='red')

        # Save the second plot as image
        worker_task_sim_counts_plot.save_plot(os.path.join(figures_folder, f"worker_task_time_taken.png"), xticks=workers_tasks, color='red')