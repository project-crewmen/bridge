import matplotlib.pyplot as plt
import numpy as np

class PiePlotter:
    def __init__(self, labels, sizes, colors=None, title=None):
        self.labels = labels
        self.sizes = sizes
        self.colors = colors
        self.title = title
        self.fig = None

    def plot(self):
        if self.fig is None:
            self.fig, _ = plt.subplots()  # Create a new figure if not created yet
        else:
            plt.figure(self.fig.number)  # Switch to the existing figure

        if self.colors is None:
            # Generate random colors if colors are not provided
            num_colors = len(self.labels)
            self.colors = plt.cm.tab10(np.arange(num_colors))

        # Plotting the pie chart
        plt.pie(self.sizes, labels=self.labels, colors=self.colors, autopct='%1.1f%%', startangle=140)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.axis('equal')
        # Adding title if provided
        if self.title:
            plt.title(self.title)
        # Show plot
        plt.show()

    def save(self, filename, dpi=200):
        if self.fig is None:
            raise ValueError("Plot not created yet. Call plot() first.")
        
        self.fig.savefig(filename, dpi=dpi)
        plt.close()