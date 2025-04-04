import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainGUI:
    def __init__(self, master):
        """Initialize the GUI with a tabbed interface at the top and split display areas below."""
        self.master = master
        self.master.title("Deep Data")
        self.master.geometry("1200x800")  # Larger window size

        # State variables
        self.data = None  # Holds the current DataFrame
        self.model = None  # Holds the trained model
        self.config = {}  # Holds method configurations

        # Create the notebook (tabbed interface) at the top
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="x", padx=10, pady=5)

        # Create main display area with a paned window below the notebook
        self.paned_window = ttk.PanedWindow(self.master, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)

        # Left side: Data display and messages
        left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(left_frame, weight=1)

        # Data table
        self.data_tree = ttk.Treeview(left_frame, show="headings")
        self.data_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Message label
        self.message_label = tk.Label(left_frame, text="", anchor="w", justify="left", bg="#f0f0f0")
        self.message_label.pack(fill="x", padx=10, pady=5)

        # Right side: Plot display
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame, weight=2)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initialize all tabs
        self.create_import_tab()
        self.create_method_tab()
        self.create_preprocessing_tab()
        self.create_visualization_tab()
        self.create_modeling_tab()
        self.create_post_analysis_tab()
        self.create_export_tab()

    # --- Import Data Tab ---
    def create_import_tab(self):
        """Create the Import Data tab for loading datasets."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Import Data")

        import_btn = ttk.Button(tab, text="Import Data", command=self.import_data)
        import_btn.pack(pady=10)

        self.has_headers = tk.BooleanVar(value=True)
        headers_check = ttk.Checkbutton(tab, text="First row as headers", variable=self.has_headers)
        headers_check.pack(pady=5)

    def import_data(self):
        """Handle data import from a file and display it."""
        from .data_import import import_data, assign_column_names
        file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx"), ("Text", "*.txt")])
        if file_path:
            try:
                self.data = import_data(file_path)
                if not self.has_headers.get():
                    self.data = assign_column_names(self.data, has_headers=False)
                else:
                    self.data = assign_column_names(self.data, has_headers=True)
                self.display_data()
                self.update_column_lists()
                self.message_label.config(text=f"Data imported successfully: {self.data.shape}")
            except Exception as e:
                self.message_label.config(text=f"Error importing data: {e}")

    def display_data(self):
        """Show the first few rows of the data in the table."""
        if self.data is not None:
            # Clear existing data
            for row in self.data_tree.get_children():
                self.data_tree.delete(row)

            # Set column headers
            self.data_tree["columns"] = list(self.data.columns)
            for col in self.data.columns:
                self.data_tree.heading(col, text=col)
                self.data_tree.column(col, width=100)

            # Insert first 5 rows
            for _, row in self.data.head().iterrows():
                self.data_tree.insert("", "end", values=list(row))

    # --- Method Storage Tab ---
    def create_method_tab(self):
        """Create the Method Storage tab for saving/loading methods."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Method Storage")

        save_btn = ttk.Button(tab, text="Save Method", command=self.save_method)
        save_btn.pack(pady=5)

        load_btn = ttk.Button(tab, text="Load Method", command=self.load_method)
        load_btn.pack(pady=5)

    def save_method(self):
        """Save the current method configuration to a file."""
        from .method_storage import save_method
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if file_path:
            save_method(self.config, file_path)
            self.message_label.config(text=f"Method saved to: {file_path}")

    def load_method(self):
        """Load a method configuration from a file."""
        from .method_storage import load_method
        file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if file_path:
            self.config = load_method(file_path)
            self.message_label.config(text=f"Method loaded from: {file_path}")

    # --- Preprocessing Tab ---
    def create_preprocessing_tab(self):
        """Create the Preprocessing tab for data transformations."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Preprocessing")

        tk.Label(tab, text="Mathematical Expression (e.g., new_col = log10(col1 * 3 + 1))").pack(pady=5)
        self.expr_entry = tk.Entry(tab, width=50)
        self.expr_entry.pack(pady=5)
        apply_btn = ttk.Button(tab, text="Apply Transformation", command=self.apply_transformation)
        apply_btn.pack(pady=5)

    def apply_transformation(self):
        """Apply a mathematical transformation to the data."""
        from .preprocessing import apply_mathematical_transformation
        if self.data is not None:
            expr = self.expr_entry.get()
            if expr:
                self.data = apply_mathematical_transformation(self.data, expr)
                self.display_data()
                self.update_column_lists()
                self.message_label.config(text=f"Transformation applied: {expr}")
            else:
                self.message_label.config(text="Please enter a valid expression")
        else:
            self.message_label.config(text="No data loaded")

    # --- Visualization Tab ---
    def create_visualization_tab(self):
        """Create the Visualization tab for plotting data."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualization")

        tk.Label(tab, text="Select column for distribution plot").pack(pady=5)
        self.dist_col = tk.StringVar()
        self.dist_col_menu = ttk.Combobox(tab, textvariable=self.dist_col, values=[])
        self.dist_col_menu.pack(pady=5)
        plot_btn = ttk.Button(tab, text="Plot Distribution", command=self.plot_distribution)
        plot_btn.pack(pady=5)

    def update_column_lists(self):
        """Update column dropdowns in tabs when data changes."""
        if self.data is not None:
            columns = list(self.data.columns)
            self.dist_col_menu['values'] = columns
            if columns:
                self.dist_col.set(columns[0])

    def plot_distribution(self):
        """Generate a distribution plot for the selected column."""
        from .visualization import plot_single_distribution
        if self.data is not None:
            col = self.dist_col.get()
            if col:
                self.ax.clear()
                self.data[col].plot(kind='hist', ax=self.ax, title=f"Distribution of {col}")
                self.canvas.draw()
                self.message_label.config(text=f"Distribution plotted for column: {col}")
            else:
                self.message_label.config(text="Please select a column")
        else:
            self.message_label.config(text="No data loaded")

    # --- Modeling Tab ---
    def create_modeling_tab(self):
        """Create the Modeling tab for training machine learning models."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Modeling")

        tk.Label(tab, text="Select Model").pack(pady=5)
        self.model_type = tk.StringVar()
        model_menu = ttk.Combobox(tab, textvariable=self.model_type, 
                                 values=["linear", "svm", "tree", "nn", "knn", "rf", "gb", "xgboost"])
        model_menu.pack(pady=5)
        self.model_type.set("linear")

        train_btn = ttk.Button(tab, text="Train Model", command=self.train_model)
        train_btn.pack(pady=5)

    def train_model(self):
        """Train a machine learning model (simplified version)."""
        from .modeling import train_model
        if self.data is not None:
            input_cols = list(self.data.columns[:-1])
            output_col = self.data.columns[-1]
            model_type = self.model_type.get()
            self.model, metrics = train_model(self.data, input_cols, output_col, model_type)
            self.message_label.config(text=f"Model trained with metrics: {metrics}")
        else:
            self.message_label.config(text="No data loaded")

    # --- Post-Analysis Tab ---
    def create_post_analysis_tab(self):
        """Create the Post-Analysis tab for SHAP analysis."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Post-Analysis")

        shap_btn = ttk.Button(tab, text="Perform SHAP Analysis", command=self.perform_shap)
        shap_btn.pack(pady=5)

    def perform_shap(self):
        """Perform SHAP analysis on the trained model."""
        from .post_analysis import perform_shap_analysis
        if self.model and self.data is not None:
            input_cols = list(self.data.columns[:-1])
            self.ax.clear()
            perform_shap_analysis(self.model, self.data, input_cols)
            self.canvas.draw()
            self.message_label.config(text="SHAP analysis completed")
        else:
            self.message_label.config(text="No model or data available")

    # --- Export Tab ---
    def create_export_tab(self):
        """Create the Export tab for saving outputs."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Export")

        export_plot_btn = ttk.Button(tab, text="Export Plot", command=self.export_plot)
        export_plot_btn.pack(pady=5)

        export_data_btn = ttk.Button(tab, text="Export Data", command=self.export_data)
        export_data_btn.pack(pady=5)

    def export_plot(self):
        """Export the current plot to a file."""
        from .exporting import export_plot
        if self.fig.axes:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if file_path:
                export_plot(self.fig, file_path)
                self.message_label.config(text=f"Plot exported to: {file_path}")
        else:
            self.message_label.config(text="No plot available to export")

    def export_data(self):
        """Export the current dataset to a file."""
        from .exporting import export_data
        if self.data is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
            if file_path:
                export_data(self.data, file_path)
                self.message_label.config(text=f"Data exported to: {file_path}")
        else:
            self.message_label.config(text="No data to export")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
