import pandas as pd
import tkinter as tk
from tkinter import ttk

def import_data(file_path):
    """
    Import data from a file based on its extension.
    
    Args:
        file_path (str): Path to the data file (.txt, .xlsx, or .csv).
    
    Returns:
        pd.DataFrame: The imported data as a pandas DataFrame.
    
    Raises:
        ValueError: If the file type is unsupported or cannot be read.
    """
    try:
        # Determine file type based on extension
        if file_path.endswith('.csv'):
            # Read only the first sheet for CSV
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            # Read only the first sheet for Excel
            df = pd.read_excel(file_path, sheet_name=0)
        elif file_path.endswith('.txt'):
            # Try different separators for text files
            separators = [';', '\t', ',', ' ']
            for sep in separators:
                try:
                    df = pd.read_csv(file_path, sep=sep)
                    # Check if the separator resulted in multiple columns
                    if len(df.columns) > 1:
                        break
                except:
                    continue
            else:
                # If no separator worked, raise an error
                raise ValueError("Could not determine the separator for the .txt file.")
        else:
            raise ValueError("Unsupported file type. Use .txt, .xlsx, or .csv files.")
        
        return df
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def assign_column_names(df, has_headers=True, parent=None):
    """
    Assign column names to the DataFrame, either using the first row or prompting the user for custom names.
    
    Args:
        df (pd.DataFrame): The DataFrame to assign column names to.
        has_headers (bool): Whether the first row should be used as column names.
        parent (tk.Tk or tk.Toplevel, optional): Parent window for the column name input dialog.
    
    Returns:
        pd.DataFrame: The DataFrame with updated column names.
    """
    if has_headers:
        # Use the first row as headers
        return df
    else:
        # If no headers, prompt the user for custom column names via a dialog
        num_cols = len(df.columns)
        # Default column names
        default_names = [f"column_{i+1}" for i in range(num_cols)]
        
        # Create a dialog window for column name input
        dialog = tk.Toplevel(parent)
        dialog.title("Enter Column Names")
        dialog.geometry("400x400")
        dialog.transient(parent)  # Make dialog modal relative to parent
        dialog.grab_set()  # Make dialog modal

        # Frame for column name inputs
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        entries = []
        for i in range(num_cols):
            label = ttk.Label(frame, text=f"Column {i+1} name:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            entry.insert(0, default_names[i])  # Default name
            entries.append(entry)
        frame.grid_columnconfigure(1, weight=1)

        # Variable to track if the user confirmed the input
        confirmed = tk.BooleanVar(value=False)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", pady=10)
        confirm_btn = ttk.Button(button_frame, text="Confirm", 
                                command=lambda: confirmed.set(True) or dialog.destroy())
        confirm_btn.pack(side="right", padx=5)
        cancel_btn = ttk.Button(button_frame, text="Cancel", 
                               command=lambda: dialog.destroy())
        cancel_btn.pack(side="right", padx=5)

        # Wait for the dialog to close
        dialog.wait_window()

        if not confirmed.get():
            raise ValueError("Column name input was cancelled by the user.")

        # Get the custom column names
        custom_names = [entry.get() for entry in entries]
        if len(custom_names) != num_cols:
            raise ValueError("Number of column names does not match number of columns.")
        
        # Assign the custom names to the DataFrame
        df.columns = custom_names
        return df
