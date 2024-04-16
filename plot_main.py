import json
import os
from dotenv import load_dotenv

from utils.plot.multi_plot import MultiPlotter
from utils.plot.pie_plot import PiePlotter

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
        initial_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["Initial NetCost"]) for entry in data]
        # bf_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BF NetCost"]) for entry in data]
        bp_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BP NetCost"]) for entry in data]
        epvm_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["EPVM NetCost"]) for entry in data]
        m3c_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["M3C NetCost"]) for entry in data]
        kube_sched_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler NetCost"]) for entry in data]
        initial_netcost = [entry["Initial NetCost"] for entry in data]
        # bf_netcost = [entry["BF NetCost"] for entry in data]
        bp_netcost = [entry["BP NetCost"] for entry in data]
        epvm_netcost = [entry["EPVM NetCost"] for entry in data]
        m3c_netcost = [entry["M3C NetCost"] for entry in data]
        kube_sched_netcost = [entry["KubeScheduler NetCost"] for entry in data]

        plt1 = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt1.plot(range(len(initial_worker_task_netcost)), initial_netcost, "Initial")
        # plt1.plot(range(len(bf_worker_task_netcost)), bf_netcost, "Brute Force")
        plt1.plot(range(len(bp_worker_task_netcost)), bp_netcost, "Bin Pack")
        plt1.plot(range(len(epvm_worker_task_netcost)), epvm_netcost, "EPVM")
        plt1.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "M3C")
        plt1.plot(range(len(kube_sched_worker_task_netcost)), kube_sched_netcost, "KubeScheduler")
        plt1.show()

        plt1.save(os.path.join(figures_folder, f"worker_task_netcost.png"))



        # Best scheduling algorithm which achives lowest net cost
        # Count occurrences where each algorithm has the lowest net cost
        init_amt = sum(1 for initial, bp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if initial < bp and initial < epvm and initial < m3c and initial < kube_sched)
        bp_amt = sum(1 for initial, bp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if bp < initial and bp < epvm and bp < m3c and bp < kube_sched)
        epvm_amt = sum(1 for initial, bp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if epvm < initial and epvm < bp and epvm < m3c and epvm < kube_sched)
        m3c_amt = sum(1 for initial, bp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if m3c < initial and m3c < epvm and m3c < bp and m3c < kube_sched)
        kube_sched_amt = sum(1 for initial, bp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if kube_sched < initial and kube_sched < epvm and kube_sched < bp and kube_sched < m3c)

        labels = ['Initial', 'BP', 'EPVM', 'M3C', 'KubeScheduler']
        sizes = [init_amt, bp_amt, epvm_amt, m3c_amt, kube_sched_amt]
        title = 'Best scheduling algorithm which achives the lowest net cost'

        pie_plt1 = PiePlotter(labels, sizes, title=title)
        pie_plt1.plot()
        pie_plt1.save(os.path.join(figures_folder, f"best_sched_algo.png"))



        # Extracting worker, task, and time taken
        # bf_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BF Computation Time"]) for entry in data]
        bp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BP Computation Time"]) for entry in data]
        epvm_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["EPVM Computation Time"]) for entry in data]
        m3c_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["M3C Computation Time"]) for entry in data]
        kube_sched_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Computation Time"]) for entry in data]
        # bf_time_taken = [entry["BF Computation Time"] for entry in data]
        bp_time_taken = [entry["BP Computation Time"] for entry in data]
        epvm_time_taken = [entry["EPVM Computation Time"] for entry in data]
        m3c_time_taken = [entry["M3C Computation Time"] for entry in data]
        kube_sched_time_taken = [entry["KubeScheduler Computation Time"] for entry in data]
        

        plt2 = MultiPlotter('(Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        # plt2.plot(range(len(bf_worker_task_time)), bf_time_taken, "Brute Force")
        plt2.plot(range(len(bp_worker_task_time)), bp_time_taken, "Bin Pack")
        plt2.plot(range(len(epvm_worker_task_time)), epvm_time_taken, "EPVM")
        plt2.plot(range(len(m3c_worker_task_time)), m3c_time_taken, "M3C")
        plt2.plot(range(len(kube_sched_worker_task_time)), kube_sched_time_taken, "KubeScheduler")
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_computation_time.png"))



        # Extracting worker, task, and total colocations
        # bf_worker_total_colocations = [(entry["Workers"], entry["Tasks"], entry["BF Total Colocations"]) for entry in data]
        bp_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["BP Total Colocations"]) for entry in data]
        epvm_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["EPVM Total Colocations"]) for entry in data]
        m3c_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["M3C Total Colocations"]) for entry in data]
        kube_sched_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Total Colocations"]) for entry in data]
        # bf_total_colocations = [entry["BF Total Colocations"] for entry in data]
        bp_total_colocations = [entry["BP Total Colocations"] for entry in data]
        epvm_total_colocations = [entry["EPVM Total Colocations"] for entry in data]
        m3c_total_colocations = [entry["M3C Total Colocations"] for entry in data]
        kube_sched_total_colocations = [entry["KubeScheduler Total Colocations"] for entry in data]
        

        plt2 = MultiPlotter('(Worker, Task) vs Total Colocations', '(Worker, Task)', 'Total Colocations')
        # plt2.plot(range(len(bf_worker_total_colocations)), bf_total_colocations, "Brute Force")
        plt2.plot(range(len(bp_worker_task_total_colocations)), bp_total_colocations, "Bin Pack")
        plt2.plot(range(len(epvm_worker_task_total_colocations)), epvm_total_colocations, "EPVM")
        plt2.plot(range(len(m3c_worker_task_total_colocations)), m3c_total_colocations, "M3C")
        plt2.plot(range(len(kube_sched_worker_task_total_colocations)), kube_sched_total_colocations, "KubeScheduler")
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_total_colocations.png"))
        