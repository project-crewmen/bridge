import json
import os
from dotenv import load_dotenv

from crewmen.crewmen import Crewmen

from utils.plot.multi_plot import MultiPlotter
from utils.plot.bar_plot import BarPlotter

from utils.latex.table import LatexTable

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

        # BinPack Scheduling Algorithm Netcosts
        plt_bp = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_bp.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_bp.plot(range(len(bp_worker_task_netcost)), bp_netcost, "bin-pack", 'blue')
        plt_bp.show()
        plt_bp.save(os.path.join(figures_folder, f"worker_task_netcost_bp.png"))

        # BinPack Scheduling Algorithm Average Netcost
        bar_plt_bp = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_bp.add_bar(x=['initial', 'bin-pack'], height=[get_avg(initial_netcost), get_avg(bp_netcost)], label="", colors=["lightblue", "blue"], show_labels=False)
        bar_plt_bp.show()
        bar_plt_bp.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_bp.png"))

        # E-PVM Scheduling Algorithm Netcosts
        plt_epvm = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_epvm.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_epvm.plot(range(len(epvm_worker_task_netcost)), epvm_netcost, "e-pvm", 'red')
        plt_epvm.show()
        plt_epvm.save(os.path.join(figures_folder, f"worker_task_netcost_epvm.png"))

        # E-PVM Scheduling Algorithm Average Netcost
        bar_plt_epvm = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_epvm.add_bar(x=['initial', 'e-pvm'], height=[get_avg(initial_netcost), get_avg(epvm_netcost)], label="", colors=["lightblue", "red"], show_labels=False)
        bar_plt_epvm.show()
        bar_plt_epvm.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_epvm.png"))

        # KubeScheduler Scheduling Algorithm Netcosts
        plt_kube_sched = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_kube_sched.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_kube_sched.plot(range(len(kube_sched_worker_task_netcost)), kube_sched_netcost, "kube-scheduler", 'green')
        plt_kube_sched.show()
        plt_kube_sched.save(os.path.join(figures_folder, f"worker_task_netcost_kube_sched.png"))

        # KubeScheduler Scheduling Algorithm Average Netcost
        bar_plt_kube_sched = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_kube_sched.add_bar(x=['initial', 'kube-scheduler'], height=[get_avg(initial_netcost), get_avg(kube_sched_netcost)], label="", colors=["lightblue", "green"], show_labels=False)
        bar_plt_kube_sched.show()
        bar_plt_kube_sched.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_kube_sched.png"))

        # M3C Scheduling Algorithm Netcosts
        plt_m3c = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_m3c.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_m3c.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "m3c", 'orange')
        plt_m3c.show()
        plt_m3c.save(os.path.join(figures_folder, f"worker_task_netcost_m3c.png"))

        # M3C Scheduling Algorithm Average Netcost
        bar_plt_m3c = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_m3c.add_bar(x=['initial', 'm3c'], height=[get_avg(initial_netcost), get_avg(m3c_netcost)], label="", colors=["lightblue", "orange"], show_labels=False)
        bar_plt_m3c.show()
        bar_plt_m3c.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_m3c.png"))


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

        # LaTeX table file (Created because I'm too lazy to copy the results each time to my thesis and update accordingly line by line)
        header_titles = ['Scheduling algorithm', 'Average Deployment ratio ($\\bar{\\gamma}$)', 'Average Network Optimization ($\\bar{\\Omega}$)']
        latex_table = LatexTable(os.path.join(figures_folder, f"worker_task_avg_deployment_ratio_and_network_optimization.tex"), 'Average Deployment ratio and Network Optimization for each Scheduling algorithm', header_titles)
        latex_table.add_row('Bin-pack', dep_ratio_bp, opt_bp)
        latex_table.add_row('\\acrshort{epvm}', dep_ratio_epvm, opt_epvm)
        latex_table.add_row('Kube-Scheduler', dep_ratio_kube_sched, opt_kube_sched)
        latex_table.add_row('\\acrshort{m3c}', dep_ratio_m3c, opt_m3c)
        latex_table.save_to_file()


        """
        Calculate Total Colocations required
        """
        # Extracting worker, task, and total colocations
        bp_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["BP Total Colocations"]) for entry in data]
        epvm_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["EPVM Total Colocations"]) for entry in data]
        kube_sched_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Total Colocations"]) for entry in data]
        m3c_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["M3C Total Colocations"]) for entry in data]
        bp_total_colocations = [entry["BP Total Colocations"] for entry in data]
        epvm_total_colocations = [entry["EPVM Total Colocations"] for entry in data]
        kube_sched_total_colocations = [entry["KubeScheduler Total Colocations"] for entry in data]
        m3c_total_colocations = [entry["M3C Total Colocations"] for entry in data]
        
        # Colocation required variations for each scheduling algorithm
        plt2 = MultiPlotter('(Worker, Task) vs Total Colocations', '(Worker, Task)', 'Total Colocations')
        plt2.plot(range(len(bp_worker_task_total_colocations)), bp_total_colocations, "bin-pack", 'blue')
        plt2.plot(range(len(epvm_worker_task_total_colocations)), epvm_total_colocations, "e-pvm", 'red')
        plt2.plot(range(len(kube_sched_worker_task_total_colocations)), kube_sched_total_colocations, "kube-scheduler", 'green')
        plt2.plot(range(len(m3c_worker_task_total_colocations)), m3c_total_colocations, "m3c", 'orange')
        plt2.show()
        plt2.save(os.path.join(figures_folder, f"worker_task_total_colocations.png"))

        # Average colocations required for each scheduling algorithm
        bar_plt_all = BarPlotter(title="Average Colocations", xlabel="Placement", ylabel="Average Colocation")
        bar_plt_all.add_bar(x=['bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[get_avg(bp_total_colocations), get_avg(epvm_total_colocations), get_avg(kube_sched_total_colocations), get_avg(m3c_total_colocations)], label="", colors=['blue', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_all.show()
        bar_plt_all.save(os.path.join(figures_folder, f"worker_task_avg_colocations.png"))



        """
        Computation Time - (Improve this further for better complexity analysis)
        """
        # Extracting worker, task, and time taken
        bp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BP Computation Time"]) for entry in data]
        epvm_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["EPVM Computation Time"]) for entry in data]
        kube_sched_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Computation Time"]) for entry in data]
        m3c_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["M3C Computation Time"]) for entry in data]
        bp_time_taken = [entry["BP Computation Time"] for entry in data]
        epvm_time_taken = [entry["EPVM Computation Time"] for entry in data]
        kube_sched_time_taken = [entry["KubeScheduler Computation Time"] for entry in data]
        m3c_time_taken = [entry["M3C Computation Time"] for entry in data]
        
        # Time taken to compute placement adapatations for each scheduling algorithm
        plt2 = MultiPlotter('(Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        plt2.plot(range(len(bp_worker_task_time)), bp_time_taken, "bin-pack", 'blue')
        plt2.plot(range(len(epvm_worker_task_time)), epvm_time_taken, "e-pvm", 'red')
        plt2.plot(range(len(kube_sched_worker_task_time)), kube_sched_time_taken, "kube-scheduler", 'green')
        plt2.plot(range(len(m3c_worker_task_time)), m3c_time_taken, "m3c", 'orange')
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_computation_time.png"))



        
        