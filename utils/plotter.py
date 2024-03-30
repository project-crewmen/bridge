import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, x_data, y_data, title='Plot', x_label='X', y_label='Y'):
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def plot(self, figsize=(8, 6), marker='', linestyle='-', color='blue', xticks=None, rotation=90):
        plt.figure(figsize=figsize)
        plt.plot(self.x_data, self.y_data, marker=marker, linestyle=linestyle, color=color)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(True)
        if xticks is not None:
            plt.xticks(ticks=self.x_data, labels=xticks, rotation=rotation)
        plt.tight_layout()
        plt.show()

    def save_plot(self, filename, figsize=(8, 6), marker='', linestyle='-', color='blue', xticks=None, rotation=90):
        plt.figure(figsize=figsize)
        plt.plot(self.x_data, self.y_data, marker=marker, linestyle=linestyle, color=color)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(True)
        if xticks is not None:
            plt.xticks(ticks=self.x_data, labels=xticks, rotation=rotation)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()