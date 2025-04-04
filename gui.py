import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt

class MainGUI:
    def __init__(self, master):
        """Initialize the main GUI window with a tabbed interface."""
        self.master = master
        self.master.title("Deep Data")
        self.master.geometry("800x600")  # Set a default window size
        
        # State variables
        self.data = None  # Holds the current DataFrame
        self.model = None  # Holds the trained model
        self.config = {}  # Holds method configurations

        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

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

        # Button to import data
        import_btn = tk.Button(tab, text="Import Data", command=self.import_data)
        import_btn.pack(pady=10)

        # Checkbox for headers
        self.has_headers = tk.BooleanVar(value=True)
        headers_check = tk.Checkbutton(tab, text="First row as headers", variable=self.has_headers)
        headers_check.pack(pady=5)

    def import_data(self):
        """Handle data import from a file."""
        from .data_import import import_data, assign_column_names
        file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx"), ("Text", "*.txt")])
        if file_path:
            self.data = import_data(file_path)
            if not self.has_headers.get():
                self.data = assign_column_names(self.data, has_headers=False)
            else:
                self.data = assign_column_names(self.data, has_headers=True)
            print("Data imported successfully:", self.data.shape)
            self.update_column_lists()  # Update column selections in other tabs

    # --- Method Storage Tab ---
    def create_method_tab(self):
        """Create the Method Storage tab for saving/loading methods."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Method Storage")

        save_btn = tk.Button(tab, text="Save Method", command=self.save_method)
        save_btn.pack(pady=5)

        load_btn = tk.Button(tab, text="Load Method", command=self.load_method)
        load_btn.pack(pady=5)

    def save_method(self):
        """Save the current method configuration to a file."""
        from .method_storage import save_method
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if file_path:
            save_method(self.config, file_path)
            print("Method saved to:", file_path)

    def load_method(self):
        """Load a method configuration from a file."""
        from .method_storage import load_method
        file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if file_path:
            self.config = load_method(file_path)
            print("Method loaded from:", file_path)

    # --- Preprocessing Tab ---
    def create_preprocessing_tab(self):
        """Create the Preprocessing tab for data transformations."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Preprocessing")

        tk.Label(tab, text="Mathematical Expression (e.g., new_col = log10(col1 * 3 + 1))").pack(pady=5)
        self.expr_entry = tk.Entry(tab, width=50)
        self.expr_entry.pack(pady=5)
        apply_btn = tk.Button(tab, text="Apply Transformation", command=self.apply_transformation)
        apply_btn.pack(pady=5)

    def apply_transformation(self):
        """Apply a mathematical transformation to the data."""
        from .preprocessing import apply_mathematical_transformation
        if self.data is not None:
            expr = self.expr_entry.get()
            if expr:
                self.data = apply_mathematical_transformation(self.data, expr)
                print("Transformation applied:", expr)
                self.update_column_lists()
            else:
                print("Please enter a valid expression")
        else:
            print("No data loaded")

    # --- Visualization Tab ---
    def create_visualization_tab(self):
        """Create the Visualization tab for plotting data."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualization")

        tk.Label(tab, text="Select column for distribution plot").pack(pady=5)
        self.dist_col = tk.StringVar()
        self.dist_col_menu = ttk.Combobox(tab, textvariable=self.dist_col, values=[])
        self.dist_col_menu.pack(pady=5)
        plot_btn = tk.Button(tab, text="Plot Distribution", command=self.plot_distribution)
        plot_btn.pack(pady=5)

    def update_column_lists(self):
        """Update column dropdowns in tabs when data changes."""
        if self.data is not None:
            columns = list(self.data.columns)
            self.dist_col_menu['values'] = columns
            if columns:
                self.dist_col.set(columns[0])
            # Add similar updates for other tabs with column selections

    def plot_distribution(self):
        """Generate a distribution plot for the selected column."""
        from .visualization import plot_single_distribution
        if self.data is not None:
            col = self.dist_col.get()
            if col:
                plot_single_distribution(self.data, col)
                print(f"Distribution plotted for column: {col}")
            else:
                print("Please select a column")
        else:
            print("No data loaded")

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
        self.model_type.set("linear")  # Default value

        train_btn = tk.Button(tab, text="Train Model", command=self.train_model)
        train_btn.pack(pady=5)

    def train_model(self):
        """Train a machine learning model (simplified version)."""
        from .modeling import train_model
        if self.data is not None:
            # Simplified: Assume all but last column are inputs, last is target
            input_cols = list(self.data.columns[:-1])
            output_col = self.data.columns[-1]
            model_type = self.model_type.get()
            self.model, metrics = train_model(self.data, input_cols, output_col, model_type)
            print("Model trained with metrics:", metrics)
        else:
            print("No data loaded")

    # --- Post-Analysis Tab ---
    def create_post_analysis_tab(self):
        """Create the Post-Analysis tab for SHAP analysis."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Post-Analysis")

        shap_btn = tk.Button(tab, text="Perform SHAP Analysis", command=self.perform_shap)
        shap_btn.pack(pady=5)

    def perform_shap(self):
        """Perform SHAP analysis on the trained model."""
        from .post_analysis import perform_shap_analysis
        if self.model and self.data is not None:
            input_cols = list(self.data.columns[:-1])  # Simplified assumption
            perform_shap_analysis(self.model, self.data, input_cols)
            print("SHAP analysis completed")
        else:
            print("No model or data available")

    # --- Export Tab ---
    def create_export_tab(self):
        """Create the Export tab for saving outputs."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Export")

        export_plot_btn = tk.Button(tab, text="Export Plot", command=self.export_plot)
        export_plot_btn.pack(pady=5)

        export_data_btn = tk.Button(tab, text="Export Data", command=self.export_data)
        export_data_btn.pack(pady=5)

    def export_plot(self):
        """Export the current plot to a file."""
        from .exporting import export_plot
        fig = plt.gcf()  # Get current figure
        if fig.axes:  # Check if there's a plot to export
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if file_path:
                export_plot(fig, file_path)
                print("Plot exported to:", file_path)
        else:
            print("No plot available to export")

    def export_data(self):
        """Export the current dataset to a file."""
        from .exporting import export_data
        if self.data is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
            if file_path:
                export_data(self.data, file_path)
                print("Data exported to:", file_path)
        else:
            print("No data to export")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
