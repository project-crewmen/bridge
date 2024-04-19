class LatexTable:
    def __init__(self, filename, caption_label, header_titles):
        self.filename = filename
        self.caption_label = caption_label
        self.header_titles = header_titles
        self.table_content = []

    def add_row(self, *args):
        self.table_content.append(args)

    def generate_table(self):
        num_columns = len(self.header_titles)
        column_specifier = "|" + "|".join(["X"] * num_columns) + "|"
        
        table = "\\begin{table}[htbp]\n"
        table += "    \\centering\n"
        table += f"    \\begin{{tabularx}}{{\\textwidth}}{{{column_specifier}}}\n"
        table += "        \\hline\n"
        table += "        " + " & ".join("\\textbf{" + title + "}" for title in self.header_titles) + "\\\\\n"
        table += "        \\hline\n"
        for row in self.table_content:
            table += "        " + " & ".join(str(item) for item in row) + "\\\\\n"
            table += "        \\hline\n"
        table += "    \\end{tabularx}\n"
        table += "    \\caption{" + self.caption_label + "}\n"
        table += "    \\label{tab:" + self.caption_label.lower().replace(" ", "_") + "}\n"
        table += "\\end{table}\n"
        return table

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            file.write(self.generate_table())
