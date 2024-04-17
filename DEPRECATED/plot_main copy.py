import json
import os
from dotenv import load_dotenv

from utils.plot.multi_plot import MultiPlotter
from utils.plot.pie_plot import PiePlotter
from utils.plot.bar_plot import BarPlotter

def get_avg(data: list):
    return sum(data) / len(data)

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
        ebp_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["EBP NetCost"]) for entry in data]
        epvm_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["EPVM NetCost"]) for entry in data]
        kube_sched_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler NetCost"]) for entry in data]
        m3c_worker_task_netcost = [(entry["Workers"], entry["Tasks"], entry["M3C NetCost"]) for entry in data]
        initial_netcost = [entry["Initial NetCost"] for entry in data]
        # bf_netcost = [entry["BF NetCost"] for entry in data]
        bp_netcost = [entry["BP NetCost"] for entry in data]
        ebp_netcost = [entry["EBP NetCost"] for entry in data]
        epvm_netcost = [entry["EPVM NetCost"] for entry in data]
        kube_sched_netcost = [entry["KubeScheduler NetCost"] for entry in data]
        m3c_netcost = [entry["M3C NetCost"] for entry in data]



        # Individual Plots
        plt_bp = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_bp.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_bp.plot(range(len(bp_worker_task_netcost)), bp_netcost, "bin-pack", 'blue')
        plt_bp.show()
        plt_bp.save(os.path.join(figures_folder, f"worker_task_netcost_bp.png"))

        bar_plt_bp = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_bp.add_bar(x=['initial', 'bin-pack'], height=[get_avg(initial_netcost), get_avg(bp_netcost)], label="", colors=["lightblue", "blue"], show_labels=False)
        bar_plt_bp.show()
        bar_plt_bp.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_bp.png"))

        
        plt_ebp = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_ebp.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_ebp.plot(range(len(ebp_worker_task_netcost)), ebp_netcost, "extended-bin-pack", 'purple')
        plt_ebp.show()
        plt_ebp.save(os.path.join(figures_folder, f"worker_task_netcost_ebp.png"))

        bar_plt_ebp = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_ebp.add_bar(x=['initial', 'extended-bin-pack'], height=[get_avg(initial_netcost), get_avg(ebp_netcost)], label="", colors=["lightblue", "purple"], show_labels=False)
        bar_plt_ebp.show()
        bar_plt_ebp.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_ebp.png"))


        plt_epvm = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_epvm.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_epvm.plot(range(len(epvm_worker_task_netcost)), epvm_netcost, "e-pvm", 'red')
        plt_epvm.show()
        plt_epvm.save(os.path.join(figures_folder, f"worker_task_netcost_epvm.png"))

        bar_plt_epvm = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_epvm.add_bar(x=['initial', 'e-pvm'], height=[get_avg(initial_netcost), get_avg(epvm_netcost)], label="", colors=["lightblue", "red"], show_labels=False)
        bar_plt_epvm.show()
        bar_plt_epvm.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_epvm.png"))


        plt_kube_sched = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_kube_sched.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_kube_sched.plot(range(len(kube_sched_worker_task_netcost)), kube_sched_netcost, "kube-scheduler", 'green')
        plt_kube_sched.show()
        plt_kube_sched.save(os.path.join(figures_folder, f"worker_task_netcost_kube_sched.png"))

        bar_plt_kube_sched = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_kube_sched.add_bar(x=['initial', 'kube-scheduler'], height=[get_avg(initial_netcost), get_avg(kube_sched_netcost)], label="", colors=["lightblue", "green"], show_labels=False)
        bar_plt_kube_sched.show()
        bar_plt_kube_sched.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_kube_sched.png"))


        plt_m3c = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt_m3c.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        plt_m3c.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "m3c", 'orange')
        plt_m3c.show()
        plt_m3c.save(os.path.join(figures_folder, f"worker_task_netcost_m3c.png"))

        bar_plt_m3c = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_m3c.add_bar(x=['initial', 'm3c'], height=[get_avg(initial_netcost), get_avg(m3c_netcost)], label="", colors=["lightblue", "orange"], show_labels=False)
        bar_plt_m3c.show()
        bar_plt_m3c.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_m3c.png"))


        # Aggregated Plot
        plt1 = MultiPlotter('(Worker, Task) vs NetCost', '(Worker, Task)', 'NetCost')
        plt1.plot(range(len(initial_worker_task_netcost)), initial_netcost, "initial", 'lightblue')
        # plt1.plot(range(len(bf_worker_task_netcost)), bf_netcost, "Brute Force")
        plt1.plot(range(len(bp_worker_task_netcost)), bp_netcost, "bin-pack", 'blue')
        plt1.plot(range(len(ebp_worker_task_netcost)), ebp_netcost, "extended-bin-pack", 'purple')
        plt1.plot(range(len(epvm_worker_task_netcost)), epvm_netcost, "e-pvm", 'red')
        plt1.plot(range(len(m3c_worker_task_netcost)), m3c_netcost, "m3c", 'green')
        plt1.plot(range(len(kube_sched_worker_task_netcost)), kube_sched_netcost, "kube-scheduler", 'orange')
        plt1.show()
        plt1.save(os.path.join(figures_folder, f"worker_task_netcost.png"))

        bar_plt_all = BarPlotter(title="Average Netcosts", xlabel="Placement", ylabel="Average Netcost")
        bar_plt_all.add_bar(x=['initial', 'bin-pack', 'e-bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[get_avg(initial_netcost), get_avg(bp_netcost), get_avg(ebp_netcost), get_avg(epvm_netcost), get_avg(kube_sched_netcost), get_avg(m3c_netcost)], label="", colors=['lightblue', 'blue', 'purple', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_all.show()
        bar_plt_all.save(os.path.join(figures_folder, f"worker_task_avg_netcosts_all.png"))



        # Best scheduling algorithm which achives lowest net cost
        # Count occurrences where each algorithm has the lowest net cost
        bp_amt = sum(1 for initial, bp, ebp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, ebp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if bp < initial and bp < ebp and bp < epvm and bp < m3c and bp < kube_sched)
        ebp_amt = sum(1 for initial, bp, ebp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, ebp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if ebp < initial and ebp < bp and ebp < epvm and ebp < m3c and ebp < kube_sched)
        epvm_amt = sum(1 for initial, bp, ebp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, ebp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if epvm < initial and epvm < bp and epvm < ebp and epvm < m3c and epvm < kube_sched)
        kube_sched_amt = sum(1 for initial, bp, ebp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, ebp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if kube_sched < initial and kube_sched < epvm and kube_sched < bp and kube_sched < ebp and kube_sched < m3c)
        m3c_amt = sum(1 for initial, bp, ebp, epvm, m3c, kube_sched in zip(initial_netcost, bp_netcost, ebp_netcost, epvm_netcost, m3c_netcost, kube_sched_netcost) if m3c < initial and m3c < epvm and m3c < bp and m3c < ebp and m3c < kube_sched)


        labels = ['bin-pack', 'extended-bin-pack', 'e-pvm', 'kube-scheduler', 'm3c']
        sizes = [bp_amt, ebp_amt, epvm_amt, kube_sched_amt, m3c_amt]
        # title = 'Percentage of achieving the lowest net cost by a Scheduling algorithm'
        title = ''

        pie_plt1 = PiePlotter(labels, sizes, title=title, colors=['blue', 'purple', 'red', 'green', 'orange'])
        pie_plt1.plot()
        pie_plt1.save(os.path.join(figures_folder, f"best_sched_algo.png"))


        """
        Total Colocations
        """
        # Extracting worker, task, and total colocations
        # bf_worker_total_colocations = [(entry["Workers"], entry["Tasks"], entry["BF Total Colocations"]) for entry in data]
        bp_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["BP Total Colocations"]) for entry in data]
        ebp_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["EBP Total Colocations"]) for entry in data]
        epvm_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["EPVM Total Colocations"]) for entry in data]
        kube_sched_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Total Colocations"]) for entry in data]
        m3c_worker_task_total_colocations = [(entry["Workers"], entry["Tasks"], entry["M3C Total Colocations"]) for entry in data]
        # bf_total_colocations = [entry["BF Total Colocations"] for entry in data]
        bp_total_colocations = [entry["BP Total Colocations"] for entry in data]
        ebp_total_colocations = [entry["EBP Total Colocations"] for entry in data]
        epvm_total_colocations = [entry["EPVM Total Colocations"] for entry in data]
        kube_sched_total_colocations = [entry["KubeScheduler Total Colocations"] for entry in data]
        m3c_total_colocations = [entry["M3C Total Colocations"] for entry in data]
        
        # Line plot
        plt2 = MultiPlotter('(Worker, Task) vs Total Colocations', '(Worker, Task)', 'Total Colocations')
        # plt2.plot(range(len(bf_worker_total_colocations)), bf_total_colocations, "Brute Force")
        plt2.plot(range(len(bp_worker_task_total_colocations)), bp_total_colocations, "bin-pack", 'blue')
        plt2.plot(range(len(ebp_worker_task_total_colocations)), ebp_total_colocations, "extended-bin-pack", 'purple')
        plt2.plot(range(len(epvm_worker_task_total_colocations)), epvm_total_colocations, "e-pvm", 'red')
        plt2.plot(range(len(kube_sched_worker_task_total_colocations)), kube_sched_total_colocations, "kube-scheduler", 'green')
        plt2.plot(range(len(m3c_worker_task_total_colocations)), m3c_total_colocations, "m3c", 'orange')
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_total_colocations.png"))

        # Bar plot
        bar_plt_all = BarPlotter(title="Average Colocations", xlabel="Placement", ylabel="Average Colocation")
        bar_plt_all.add_bar(x=['bin-pack', 'e-bin-pack', 'e-pvm', 'kube-scheduler', 'm3c'], height=[get_avg(bp_total_colocations), get_avg(ebp_total_colocations), get_avg(epvm_total_colocations), get_avg(kube_sched_total_colocations), get_avg(m3c_total_colocations)], label="", colors=['blue', 'purple', 'red', 'green', 'orange'], show_labels=False)
        bar_plt_all.show()
        bar_plt_all.save(os.path.join(figures_folder, f"worker_task_avg_colocations.png"))

        """
        Computation Time
        """
        # Extracting worker, task, and time taken
        # bf_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BF Computation Time"]) for entry in data]
        bp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["BP Computation Time"]) for entry in data]
        ebp_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["EBP Computation Time"]) for entry in data]
        epvm_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["EPVM Computation Time"]) for entry in data]
        kube_sched_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["KubeScheduler Computation Time"]) for entry in data]
        m3c_worker_task_time = [(entry["Workers"], entry["Tasks"], entry["M3C Computation Time"]) for entry in data]
        # bf_time_taken = [entry["BF Computation Time"] for entry in data]
        bp_time_taken = [entry["BP Computation Time"] for entry in data]
        ebp_time_taken = [entry["EBP Computation Time"] for entry in data]
        epvm_time_taken = [entry["EPVM Computation Time"] for entry in data]
        kube_sched_time_taken = [entry["KubeScheduler Computation Time"] for entry in data]
        m3c_time_taken = [entry["M3C Computation Time"] for entry in data]
        
        # Line plot
        plt2 = MultiPlotter('(Worker, Task) vs Computation Time', '(Worker, Task)', 'Computation Time(seconds)')
        # plt2.plot(range(len(bf_worker_task_time)), bf_time_taken, "Brute Force")
        plt2.plot(range(len(bp_worker_task_time)), bp_time_taken, "bin-pack", 'blue')
        plt2.plot(range(len(ebp_worker_task_time)), ebp_time_taken, "extended-bin-pack", 'purple')
        plt2.plot(range(len(epvm_worker_task_time)), epvm_time_taken, "e-pvm", 'red')
        plt2.plot(range(len(kube_sched_worker_task_time)), kube_sched_time_taken, "kube-scheduler", 'green')
        plt2.plot(range(len(m3c_worker_task_time)), m3c_time_taken, "m3c", 'orange')
        plt2.show()

        plt2.save(os.path.join(figures_folder, f"worker_task_computation_time.png"))



        
        