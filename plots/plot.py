import json
import os
import matplotlib.pyplot as plt

# Read data from JSON file
file_name =  f"test_2024-02-29_14-07-22"
with open((os.path.join("test_results", f"{file_name}.json")), 'r') as file:
    data = json.load(file)

# Extracting worker, task, and simulation count
worker_task_simulations = [(entry["Workers"], entry["Tasks"], entry["Simulations"]) for entry in data]
workers_tasks = [(entry["Workers"], entry["Tasks"]) for entry in data]
simulations = [entry["Simulations"] for entry in data]

# Plotting first figure: Worker & Task vs Simulation Count
plt.figure(figsize=(8, 6))
plt.plot(range(len(worker_task_simulations)), simulations, marker='o', linestyle='-', color='blue')
plt.title('(Worker, Task) vs Simulation Count')
plt.xlabel('(Worker, Task)')
plt.ylabel('Simulation Count')
plt.xticks(range(len(worker_task_simulations)), workers_tasks, rotation=90)  # Set x-axis labels
plt.grid(True)
plt.tight_layout()

# Save the first plot as image
plt.savefig((os.path.join("figures", f"worker_task_simulation_count_{file_name}.png")))

# Display the first plot
plt.show()

# Extracting worker, task, and time taken
worker_task_time = [(entry["Workers"], entry["Tasks"], entry["Time_taken"]) for entry in data]
time_taken = [entry["Time_taken"] for entry in data]

# Plotting second figure: Worker & Task vs Time Taken
plt.figure(figsize=(8, 6))
plt.plot(range(len(worker_task_time)), time_taken, marker='o', linestyle='-', color='red')
plt.title('(Worker, Task) vs Computation Time')
plt.xlabel('(Worker, Task)')
plt.ylabel('Computation Time(seconds)')
plt.xticks(range(len(worker_task_time)), workers_tasks, rotation=90)  # Set x-axis labels
plt.grid(True)
plt.tight_layout()

# Save the second plot as image
plt.savefig((os.path.join("figures", f"worker_task_time_taken_{file_name}.png")))

# Display the second plot
plt.show()

