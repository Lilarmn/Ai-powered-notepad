import tkinter as tk
from tkinter import filedialog
import customtkinter as ct
from tkinter.font import Font
from tklinenums import TkLineNumbers
from tkinter import ttk
from Intellisense import textIq
import re
from SearchFrame import SearchWindow
from TranscribFrame import AudioRecorderApp


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        # Set appearance and theme
        ct.set_appearance_mode("System")
        ct.set_default_color_theme("blue")

        # Set up main window
        self.title("App")
        self.geometry("800x600")

        # Configuration
        self.font_size = 12
        self.toolbar_color = '#222831'
        self.line_numbers_color = '#222831'
        self.line_numbers_font_color = '#EEEEEE'
        self.text_box_color = '#393E46'
        self.text_box_font_color = '#BDCDD6'
        self.text_font = Font(family="Verdana", size=self.font_size)

        # Create container
        self.container = ct.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Add toolbar and editor
        self.add_toolbars()
        self.editor()

    def add_toolbars(self):
        # Create a custom menu bar frame
        menu_bar = tk.Frame(self.container, bg=self.toolbar_color, height=30)
        menu_bar.pack(fill="x", side="top")

        # File menu
        file_menu = tk.Menubutton(menu_bar, text="File", bg='#00ADB5', fg="white", font=("Verdana", 11))
        file_menu.pack(side="left", padx=5)

        # File menu dropdown
        file_menu_dropdown = tk.Menu(file_menu, tearoff=0, bg='#00ADB5', fg="white", font=("Verdana", 11))
        file_menu_dropdown.add_command(label="New", command=lambda: self.toolbar_functions("new"))
        file_menu_dropdown.add_command(label="Open...", command=lambda: print("Open File"))
        file_menu_dropdown.add_separator()
        file_menu_dropdown.add_command(label="Save As...", command=self.save_as_file)
        file_menu_dropdown.add_separator()
        file_menu_dropdown.add_command(label="Exit", command=self.destroy)
        file_menu.config(menu=file_menu_dropdown)

        # Edit menu
        edit_menu = tk.Menubutton(menu_bar, text="Edit", bg='#00ADB5', fg="white", font=("Verdana", 11))
        edit_menu.pack(side="left", padx=5)

        # Edit menu dropdown
        edit_menu_dropdown = tk.Menu(edit_menu, tearoff=0, bg='#00ADB5', fg="white", font=("Verdana", 11))
        edit_menu_dropdown.add_command(label="Increase Font", command=lambda: self.change_font_size(2))
        edit_menu_dropdown.add_command(label="Decrease Font", command=lambda: self.change_font_size(-2))
        edit_menu_dropdown.add_command(label="Undo", command=lambda: print("Undo Action"))
        edit_menu_dropdown.add_command(label="Redo", command=lambda: print("Redo Action"))
        edit_menu_dropdown.add_command(label="Search", command=self.open_search_window)
        edit_menu.config(menu=edit_menu_dropdown)

    def toolbar_functions(self, name):
        if name == "new":
            self.destroy()
            run()

    def editor(self):
        # Create a frame for the editor and line numbers
        editor_frame = tk.Frame(self.container)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize text widget with scrollbars
        self.initialize_text_widget(editor_frame)

        # Initialize line numbers
        self.initialize_line_numbers(editor_frame)

        # Apply features to the editor
        self.apply_editor_features()

    def initialize_text_widget(self, parent):
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical")
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal")
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Create text widget
        self.text_box = tk.Text(
            parent,
            wrap="word",
            undo=True,
            foreground=self.text_box_font_color,
            font=self.text_font,
            background=self.text_box_color,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
        )
        self.text_box.pack(side="right", fill="both", expand=True)
        self.text_box.tag_config("highlight", foreground="#C890A7")

        # Configure scrollbars
        v_scrollbar.config(command=self.text_box.yview)
        h_scrollbar.config(command=self.text_box.xview)

    def initialize_line_numbers(self, parent):
        # Create line numbers widget
        self.line_numbers = TkLineNumbers(
            parent,
            self.text_box,
            justify="center",
            colors=(self.line_numbers_font_color, self.line_numbers_color),
        )
        self.line_numbers.pack(fill="y", side="left")

    def apply_editor_features(self):
        # Bind keyboard shortcuts and events
        self.text_box.bind("<Return>", self.on_enter_key)
        self.text_box.bind("<Control-s>", self.save_as_file)
        self.text_box.bind("<Control-Shift-plus>", lambda event: self.change_font_size(2))
        self.text_box.bind("<Control-minus>", lambda event: self.change_font_size(-2))
        self.text_box.bind("<Control-Return>",self.intellisense)
        self.text_box.bind("<Control-f>",self.open_search_window)
        self.text_box.bind("<Control-t>",self.open_transcribe_window)

        # Redraw line numbers whenever the text is modified
        self.text_box.bind(
            "<<Modified>>",
            lambda event: self.after_idle(self.line_numbers.redraw),
            add=True,
        )

    def on_enter_key(self, event):
        # Insert a new line and redraw line numbers
        self.text_box.insert("insert", "\n")
        self.line_numbers.redraw()

        #make syntax blue
        self.text_box.tag_remove("highlight", "1.0", tk.END)
        content = self.text_box.get("1.0", tk.END)
        matches = re.finditer(r"#(.*?)#", content)

        for match in matches:
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            self.text_box.tag_add("highlight", start_idx, end_idx)

        return "break"

    def save_as_file(self, event=None):
        # Open file dialog for saving
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save As"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_box.get("1.0", tk.END).strip())
                print(f"File saved successfully: {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
        return "break"

    def change_font_size(self, increment):
        # Increase or decrease font size
        self.font_size = max(8, self.font_size + increment)
        self.text_font.configure(size=self.font_size)
        self.text_box.configure(font=self.text_font)

    def intellisense(self,event):
        current_text = self.text_box.get("1.0", tk.END).strip()  # Get text from textbox
        updated_text = textIq(current_text)  # Process the text
        self.text_box.delete("1.0", tk.END)  # Clear the textbox
        self.text_box.insert(tk.END, updated_text)

    def process_search(self, search_term):
        # Handle the search term (e.g., highlight it in the editor or perform other actions)
        print(f"Searching for: {search_term}")
        # Example: Highlight search term in the editor
        if search_term:
            self.text_box.tag_remove("highlight", "1.0", tk.END)  # Remove previous highlights
            start_pos = "1.0"
            while True:
                start_pos = self.text_box.search(search_term, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.text_box.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_box.tag_config("highlight", background="yellow", foreground="black")

    def open_search_window(self,event=None):
        search_window = SearchWindow(self)
        search_window.mainloop()

    def open_transcribe_window(self,event=None):
        self.AudioRecorder = AudioRecorderApp(self)
        self.AudioRecorder.mainloop()

    def replace_all(self, search_term,new_term):
        print(f"Searching for: {search_term}")
        # Example: Highlight search term in the editor
        if search_term and new_term:
            new_text = self.text_box.get("1.0", tk.END).strip().replace(search_term,new_term)
            self.text_box.delete("1.0", tk.END)  # Clear the textbox
            self.text_box.insert(tk.END, new_text)

    def insert_transcribe_text(self,text):
        self.text_box.insert(tk.END, text)

def run():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    run()
