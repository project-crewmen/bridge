import matplotlib.pyplot as plt

class BarPlotter:
    def __init__(self, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.bars = []  # List of all bars to be plotted
        self.fig = None  # Store the figure handle

    def add_bar(self, x, height, label, colors=None, show_labels=False, bar_width=0.6):
        if colors is None:
            colors = 'blue'  # Default color
        self.bars.append((x, height, label, colors, show_labels, bar_width))

    def show(self):
        if self.fig is None:
            self.fig, _ = plt.subplots()  # Create a new figure if not created yet
        else:
            plt.figure(self.fig.number)  # Switch to the existing figure

        for x, height, label, colors, show_labels, bar_width in self.bars:
            if isinstance(colors, str):
                colors = [colors] * len(x)  # If a single color is provided, repeat it for each bar
            for xpos, h, c in zip(x, height, colors):
                plt.bar(xpos, h, label=label if show_labels else None, color=c, width=bar_width)

        # Add title and labels
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # Add legend if any group has labels enabled
        for _, _, _, _, show_labels, _ in self.bars:
            if show_labels:
                plt.legend()
                break

        # Show plot
        plt.show()

    def save(self, filename, dpi=200):
        if self.fig is None:
            raise ValueError("Plot not created yet. Call show() first.")

        self.fig.savefig(filename, dpi=dpi)
        plt.close()