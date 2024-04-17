import matplotlib.pyplot as plt
import numpy as np

# Data for each algorithm
algorithms = ['A1', 'A2', 'A3', 'A4']
total_colocations = [10, 8, 9, 5]
average_netcost_reduction = [10, 8, 4, 5]

# Set the width of the bars
bar_width = 0.35

# Set the position of the bars on the x-axis
x = np.arange(len(algorithms))

# Create the bar plot
fig, ax = plt.subplots()
bars1 = ax.bar(x - bar_width/2, total_colocations, bar_width, label='Total Colocations')
bars2 = ax.bar(x + bar_width/2, average_netcost_reduction, bar_width, label='Average Net Cost Reduction')

# Add labels and legend
ax.set_xlabel('Algorithms')
ax.set_ylabel('Values')
ax.set_title('Comparison of Algorithms')
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()

# Show the plot
plt.grid(True)
plt.show()
