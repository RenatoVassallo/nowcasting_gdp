import os

# Define the base directory for the project
dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input directories
dir_input_raw       = os.path.join(dir_base, 'input', 'raw')
dir_input_cleaned   = os.path.join(dir_base, 'input', 'cleaned')

# Output directories
dir_output          = os.path.join(dir_base, 'output')

# Helper function to ensure directories exist
def ensure_directories():
    for directory in [dir_input_raw, dir_input_cleaned, dir_output]:
        os.makedirs(directory, exist_ok=True)

# Call the function to create directories if they don't exist
ensure_directories()