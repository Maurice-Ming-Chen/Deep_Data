# Deep_Data/__init__.py

# Import the main GUI class
from .gui import MainGUI

# Import data import functions
from .data_import import import_data

# Import method storage functions
from .method_storage import save_method, load_method, apply_method

# Import preprocessing functions
from .preprocessing import (
    apply_mathematical_transformation,
    truncate_data,
    fill_missing_values,
    encode_categorical
)

# Import visualization functions
from .visualization import (
    plot_single_distribution,
    plot_cross_relationship,
    reduce_and_plot
)

# Import modeling functions
from .modeling import (
    train_model,
    tune_hyperparameters,
    plot_predictions
)

# Import post-analysis functions
from .post_analysis import perform_shap_analysis

# Import exporting functions
from .exporting import (
    export_plot,
    export_data,
    export_model,
    export_method,
    export_shap_data
)

# Optional package metadata
__version__ = "0.1.0"
__author__ = "Your Name"
