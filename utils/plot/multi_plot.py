import matplotlib.pyplot as plt

class MultiPlotter:
    def __init__(self, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.lines = [] # List of all lines to be plot
        self.fig = None   # Store the figure handle

    def plot(self, x, y, label):
        self.lines.append((x, y, label))

    def show(self):
        if self.fig is None:
            self.fig, _ = plt.subplots()  # Create a new figure if not created yet
        else:
            plt.figure(self.fig.number)  # Switch to the existing figure

        for x, y, label in self.lines:
            plt.plot(x, y, label=label)

        # Add title and labels
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # Add legend
        plt.legend()

        # Show plot
        plt.show()

    def save(self, filename, dpi=200):
        if self.fig is None:
            raise ValueError("Plot not created yet. Call show() first.")

        self.fig.savefig(filename, dpi=dpi)
        plt.close()
