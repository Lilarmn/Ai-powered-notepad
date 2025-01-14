import customtkinter as ct
import tkinter as tk
import re

class SearchWindow(ct.CTk):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Reference to the main application
        self.replace_widgets = []  # Store replace widgets for easy removal
        self.initialize()

    def initialize(self):
        ct.set_appearance_mode("System")
        ct.set_default_color_theme("blue")

        self.title("Search App")
        self.geometry("500x300")
        self.resizable(False, False)

        self.mainFrame = ct.CTkFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label = ct.CTkLabel(self.mainFrame, text="Enter your search term:", font=("Arial", 18))
        self.label.pack(pady=(10, 5))

        self.entry = ct.CTkEntry(self.mainFrame, font=("Arial", 12), placeholder_text="Search...")
        self.entry.pack(pady=10)

        self.exitButton = ct.CTkButton(self.mainFrame, text="Exit", font=("Arial", 10), command=self.exit_app, width=80)
        self.exitButton.pack(side=tk.LEFT, padx=(30, 10), pady=20)

        self.searchButton = ct.CTkButton(
            self.mainFrame,
            text="Search",
            font=("Arial", 12),
            command=self.perform_search,
            width=90
        )
        self.searchButton.pack(side=tk.LEFT, padx=(10, 30), pady=20)

        self.replace_check_box = ct.CTkCheckBox(
            self.mainFrame,
            text="Replace",
            font=("Arial", 8),
            command=self.toggle_replace_widgets
        )
        self.replace_check_box.pack(side=tk.LEFT)

    def toggle_replace_widgets(self):
        # If checked, add Replace button and entry
        if self.replace_check_box.get():
            self.add_replace_widgets()
        else:
            self.remove_replace_widgets()

    def add_replace_widgets(self):
        # Add "Replace With" label
        self.replace_label = ct.CTkLabel(self.mainFrame, text="Replace with:", font=("Arial", 12))
        self.replace_label.pack(pady=(10, 5))
        self.replace_widgets.append(self.replace_label)

        # Add "Replace With" entry box
        self.replace_entry = ct.CTkEntry(self.mainFrame, font=("Arial", 12), placeholder_text="Replace with...")
        self.replace_entry.pack(pady=10)
        self.replace_widgets.append(self.replace_entry)

        # Add Replace All button
        self.replaceButton = ct.CTkButton(
            self.mainFrame,
            text="Replace All",
            font=("Arial", 12),
            command=self.perform_replace,
            width=70
        )
        self.replaceButton.pack(pady=20)
        self.replace_widgets.append(self.replaceButton)

    def remove_replace_widgets(self):
        # Destroy all replace widgets
        for widget in self.replace_widgets:
            widget.destroy()
        self.replace_widgets = []

    def perform_search(self):
        search_term = self.entry.get()  # Get the search term
        self.main_app.process_search(search_term)  # Call method in main app
        self.destroy()  # Close the search window

    def perform_replace(self):
        search_term = self.entry.get()  # Get the search term
        replace_with = self.replace_entry.get()  # Get the replace text
        self.main_app.replace_all(search_term, replace_with)  # Call method in main app
        self.destroy()

    def exit_app(self):
        self.destroy()
