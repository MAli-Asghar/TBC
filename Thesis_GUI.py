import tkinter as tk
from tkinter import ttk, filedialog

import test_benches


class FourPartGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Four Part GUI")

        # Configure the grid layout
        self.root.rowconfigure([0, 1], weight=1, minsize=100)
        self.root.columnconfigure([0, 1], weight=1, minsize=200)

        # Create frames for each section
        self.frame1 = tk.Frame(root, bg="lightblue")
        self.frame2 = tk.Frame(root, bg="lightgreen")
        self.frame3 = tk.Frame(root, bg="lightyellow")
        self.frame4 = tk.Frame(root, bg="lightcoral")

        # Place frames in the grid
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=0, column=1, sticky="nsew")
        self.frame3.grid(row=1, column=0, sticky="nsew")
        self.frame4.grid(row=1, column=1, sticky="nsew")

        # Add labels to each frame
        self.label1 = tk.Label(self.frame1, text="Section 1", bg="lightblue")
        self.label2 = tk.Label(self.frame2, text="Section 2", bg="lightgreen")
        self.label3 = tk.Label(self.frame3, text="Section 3", bg="lightyellow")
        self.label4 = tk.Label(self.frame4, text="Section 4", bg="lightcoral")

        self.label1.pack(expand=True)
        self.label2.pack(expand=True)
        self.label3.pack(expand=True)
        self.label4.pack(expand=True)

        # Dictionary with options and associated values
        self.options_dict = test_benches.projects

        # Add a drop-down button to Section 1
        self.options = list(self.options_dict.keys())
        self.dropdown = ttk.Combobox(self.frame1, values=self.options, state="readonly")
        self.dropdown.place(x=10, y=10)

        # Add a submit button to disable the dropdown and show values
        self.submit_button = tk.Button(self.frame1, text="Submit", command=self.disable_dropdown)
        self.submit_button.place(x=10, y=50)

        # Add a re-submit button to re-enable the dropdown
        self.resubmit_button = tk.Button(self.frame1, text="Re-Submit", command=self.enable_dropdown)
        self.resubmit_button.place(x=10, y=90)

        # Label to display the values associated with the selected option
        self.values_label = tk.Label(self.frame1, text="", bg="lightblue")
        self.values_label.place(x=10, y=130)

        # Add a button to upload three Automation Desk project folders
        self.upload_button = tk.Button(self.frame1, text="Upload Folders", command=self.upload_folders)
        self.upload_button.place(x=10, y=170)

        # Labels to display the folder names and dropdowns for each folder
        self.folder_labels = []
        self.folder_dropdowns = []
        self.selected_values = []
        self.previous_selections = {}
        self.selected_key = None

    def disable_dropdown(self):
        selected_option = self.dropdown.get()

        if selected_option:
            print(f"Selected option: {selected_option}")

            # Disable the dropdown after clicking submit
            self.dropdown.config(state="disabled")

            # Store the selected key
            self.selected_key = selected_option

            # Display the values associated with the selected option
            values = "\n".join(self.options_dict[selected_option])
            self.values_label.config(text=f"Values:\n{values}")

    def enable_dropdown(self):
        # Re-enable the dropdown
        self.dropdown.config(state="readonly")

        # Clear the values label
        self.values_label.config(text="")

        # Clear the folder labels and dropdowns
        for label in self.folder_labels:
            label.destroy()
        for dropdown in self.folder_dropdowns:
            dropdown.destroy()

        self.folder_labels = []
        self.folder_dropdowns = []
        self.selected_values = []
        self.previous_selections = {}
        self.selected_key = None

    def upload_folders(self):
        folder_paths = []

        for i in range(3):
            folder_path = filedialog.askdirectory(title=f"Select Folder {i + 1}")
            if folder_path:
                folder_paths.append(folder_path)
                folder_name = folder_path.split("/")[-1]
                print(f"Uploaded Folder {i + 1}: {folder_name}")

                label = tk.Label(self.frame1, text=f"Folder {i + 1}: {folder_name}", bg="lightblue")
                label.place(x=10, y=210 + i * 30)
                self.folder_labels.append(label)

                dropdown = ttk.Combobox(self.frame1, values=self.get_available_values(), state="readonly")
                dropdown.place(x=200, y=210 + i * 30)
                dropdown.bind("<<ComboboxSelected>>", self.update_dropdowns)
                self.folder_dropdowns.append(dropdown)
                self.previous_selections[dropdown] = None

    def get_available_values(self):
        # Get values that are not yet selected
        if self.selected_key:
            return [value for value in self.options_dict[self.selected_key] if value not in self.selected_values]
        return []

    def update_dropdowns(self, event):
        dropdown = event.widget
        selected_value = dropdown.get()

        # Remove the previous selection from the selected values
        if self.previous_selections[dropdown]:
            self.selected_values.remove(self.previous_selections[dropdown])

        # Add the new selection to the selected values
        self.selected_values.append(selected_value)

        # Update the previous selection for this dropdown
        self.previous_selections[dropdown] = selected_value

        # Update all dropdowns with the new available values
        for dropdown in self.folder_dropdowns:
            current_value = dropdown.get()
            dropdown.config(values=self.get_available_values())
            if current_value:
                dropdown.set(current_value)


if __name__ == "__main__":
    root = tk.Tk()
    app = FourPartGUI(root)
    root.mainloop()