import json
from tkinter import ttk


# Default settings
default_settings = {
    "bg_color": "#FFFFFF",
    "text_color": "#000000"
}

# Global variable to store the settings data
settings_data = {}

def configure_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Title.TLabel', font=('Arial', 12, 'bold'), background='#0066FF', foreground='#FFFFFF')
    style.configure('TLabel', background='#FFFFFF', foreground='#000000')

def load_settings():
    try:
        with open("unicodeViewer.settings", "r") as f:
            loaded_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is invalid, use default settings
        loaded_settings = {}

    # Update the settings data with loaded settings or default settings
    settings_data.update(default_settings)
    settings_data.update(loaded_settings)

    # Print the loaded settings for verification
    print(settings_data)


# Call the load_settings() function to load the settings
load_settings()