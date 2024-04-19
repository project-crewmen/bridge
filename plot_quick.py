import json
import os
from dotenv import load_dotenv

from crewmen.crewmen import Crewmen

from utils.plot.multi_plot import MultiPlotter
from utils.plot.bar_plot import BarPlotter

def get_avg(data: list):
    return sum(data) / len(data)

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Access environment variables
    sim_result_to_plot = os.getenv("TARGET_LOG")

    print(sim_result_to_plot)

    wm = Crewmen()

    # Read data from JSON file
    with open((os.path.join("out/sim_results", f"{sim_result_to_plot}.json")), 'r') as file:
        data = json.load(file)

        # Create a new folder for figures if it doesn't exist
        figures_folder = os.path.join("out/figs", sim_result_to_plot)
        if not os.path.exists(figures_folder):
            os.makedirs(figures_folder)


        """
        Evaluation of each scheduling algorithm
        """
        # Extracting worker, task, and simulation count
        workers_tasks = [(entry["Workers"], entry["Tasks"]) for entry in data]
        initial_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["Initial NetCost"]) for entry in data]
        bp_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["BP NetCost"]) for entry in data]
        epvm_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["EPVM NetCost"]) for entry in data]
        kube_sched_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler NetCost"]) for entry in data]
        m3c_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["M3C NetCost"]) for entry in data]
        initial_netcost = [entry["Initial NetCost"] for entry in data]
        bp_netcost = [entry["BP NetCost"] for entry in data]
        epvm_netcost = [entry["EPVM NetCost"] for entry in data]
        kube_sched_netcost = [entry["KubeScheduler NetCost"] for entry in data]
        m3c_netcost = [entry["M3C NetCost"] for entry in data]


        """
        Aggregate Plots of Scheduling algorithms
        """
        # Netcost variations of each algorithm
        plt1 = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt1.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt1.plot(range(len(bp_worker_task_netcost)), bp_netcost, "bin-pack", 'blue')
        plt1.plot(range(len(epvm_worker_task_netcost)), epvm_netcost, "e-pvm", 'red')
        plt1.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "m3c", 'green')
        plt1.plot(range(len(kube_sched_worker_task_netcost)), kube_sched_netcost, "kube-scheduler", 'orange')
        plt1.show()
        plt1.save(os.path.join(figures_folder, f"worker_task_netcost.png"))

        # Average netcosts for each algorithm
        bar_plt_all = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_all.add_bar(x=['initial', 'bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[get_avg(initial_netcost), get_avg(bp_netcost), get_avg(epvm_netcost), get_avg(kube_sched_netcost), get_avg(m3c_netcost)], label="", colors=['lightblue', 'blue', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_all.show()
        bar_plt_all.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_all.png"))


        """
        Calculating Average network optimizations
        """
        # Calculate average deployment ratio for each scheduling algorithms
        bar_plt_dep_ratio = BarPlotter(title="Average Deployment Ratio", xlabel="Scheduling Algorithm", ylabel="Average Deployment Ratio")
        dep_ratio_bp = wm.deployment_ratio(get_avg(initial_netcost), get_avg(bp_netcost))
        dep_ratio_epvm = wm.deployment_ratio(get_avg(initial_netcost), get_avg(epvm_netcost))
        dep_ratio_kube_sched = wm.deployment_ratio(get_avg(initial_netcost), get_avg(kube_sched_netcost))
        dep_ratio_m3c = wm.deployment_ratio(get_avg(initial_netcost), get_avg(m3c_netcost))
        bar_plt_dep_ratio.add_bar(x=['bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[dep_ratio_bp, dep_ratio_epvm, dep_ratio_kube_sched, dep_ratio_m3c], label="", colors=['blue', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_dep_ratio.show()
        bar_plt_dep_ratio.save(os.path.join(figures_folder, f"worker_task_avg_deployment_ratio.png"))

        # Calculate average network optimization for each scheduling algorithms
        bar_plt_optimization = BarPlotter(title="Average Network Optimization", xlabel="Scheduling Algorithm", ylabel="Average Network Optimization")
        opt_bp = wm.network_optimization(dep_ratio_bp)
        opt_epvm = wm.network_optimization(dep_ratio_epvm)
        opt_kube_sched = wm.network_optimization(dep_ratio_kube_sched)
        opt_m3c = wm.network_optimization(dep_ratio_m3c)
        bar_plt_optimization.add_bar(x=['bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[opt_bp, opt_epvm, opt_kube_sched, opt_m3c], label="", colors=['blue', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_optimization.show()
        bar_plt_optimization.save(os.path.join(figures_folder, f"worker_task_avg_network_optimization.png"))



        
        