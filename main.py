import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import ttk
import threading
import json
import settings
import logger as uvLogger

class UnicodeViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unicode Character Viewer")
        settings.configure_style()
        self.create_title_bar()
        self.create_ui()
        self.start_x = 0
        self.start_y = 0

        # Center the window on the screen
        self.center_window()

    def create_title_bar(self):
        self.title_bar = ttk.Frame(self.root)
        self.title_bar.pack(fill='x')

        # Bind mouse events for dragging functionality
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag)

        # Create title label
        self.title_label = ttk.Label(self.title_bar, text="Unicode Character Viewer", style='Title.TLabel')
        self.title_label.pack(side='left')

        # Create settings button
        self.settings_button = ttk.Button(self.title_bar, text='Settings', command=self.open_settings)
        self.settings_button.pack(side='right')

        # Create reload button
        self.reload_button = ttk.Button(self.title_bar, text='Reload', command=self.load_unicode_characters)
        self.reload_button.pack(side='right')
        
        # Create close button
        self.close_button = ttk.Button(self.title_bar, text='X', command=self.close_application)
        self.close_button.pack(side='right')

    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def drag(self, event):
        deltax = event.x - self.start_x
        deltay = event.y - self.start_y

        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def create_ui(self):
        self.text_area = scrolledtext.ScrolledText(self.root, width=80, height=30)
        self.text_area.pack()

        self.load_button = ttk.Button(self.root, text="Load Unicode Characters", command=self.load_unicode_characters)
        self.load_button.pack()
        uvLogger.debug("UI created successfully")



    def load_unicode_characters(self):
        self.text_area.delete("1.0", tk.END)
        thread = threading.Thread(target=self.populate_text_area)
        thread.start()

        # Log a debug message
        uvLogger.debug("Loading Unicode characters")

    def populate_text_area(self):
        for i in range(0x100):
            character = chr(i)
            self.text_area.insert(tk.END, character)

        # Log an info message
        uvLogger.info("Unicode characters loaded successfully")

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x200")

        self.bg_color_label = ttk.Label(self.settings_window, text="Background Color")
        self.bg_color_label.pack()
        self.bg_color_picker = tk.StringVar()
        self.bg_color_picker.set(settings.settings_data.get("bg_color", "#FFFFFF"))
        self.bg_color_entry = ttk.Entry(self.settings_window, textvariable=self.bg_color_picker)
        self.bg_color_entry.pack()

        self.text_color_label = ttk.Label(self.settings_window, text="Text Color")
        self.text_color_label.pack()

        self.text_color_picker = tk.StringVar()
        self.text_color_picker.set(settings.settings_data.get("text_color", "#000000"))
        self.text_color_entry = ttk.Entry(self.settings_window, textvariable=self.text_color_picker)
        self.text_color_entry.pack()

        # Create a logging checkbox
        self.logging_var = tk.IntVar()
        self.logging_var.set(settings.settings_data.get("enable_logging", 0))
        self.logging_checkbox = ttk.Checkbutton(self.settings_window, text="Enable Logging",
                                                variable=self.logging_var, onvalue=1, offvalue=0)
        self.logging_checkbox.pack()

        self.save_button = ttk.Button(self.settings_window, text="Save", command=self.save_settings)
        self.save_button.pack()

        # Center the settings window on the screen
        self.settings_window.update()
        screen_width = self.settings_window.winfo_screenwidth()
        screen_height = self.settings_window.winfo_screenheight()
        x = (screen_width / 2) - (self.settings_window.winfo_width() / 2)
        y = (screen_height / 2) - (self.settings_window.winfo_height() / 2)
        self.settings_window.geometry(f"+{int(x)}+{int(y)}")
        uvLogger.debug("Settings window opened")

    def save_settings(self):
        settings.settings_data["bg_color"] = self.bg_color_picker.get()
        settings.settings_data["text_color"] = self.text_color_picker.get()
        settings.settings_data["enable_logging"] = self.logging_var.get()

        with open("unicodeViewer.settings", "w") as f:
            json.dump(settings.settings_data, f)

        self.settings_window.destroy()

        self.apply_settings()

    def apply_settings(self):
        style = ttk.Style()
        style.configure('TLabel', background=settings.settings_data.get("bg_color", "#FFFFFF"),
                        foreground=settings.settings_data.get("text_color", "#000000"))

        # Configure logger based on enable_logging setting
        if settings.settings_data.get("enable_logging", 0):
            uvLogger.enable_logging()
        else:
            uvLogger.disable_logging()

    def close_application(self):
        self.root.destroy()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width - self.root.winfo_reqwidth()) / 2)
        y = int((screen_height - self.root.winfo_reqheight()) / 2)

        self.root.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    app = UnicodeViewerApp(root)
    root.overrideredirect(True)
    root.mainloop()

if __name__ == "__main__":
    main()