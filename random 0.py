import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import math
import time
import sys

# Increase recursion limit (default is 1000, which might not be enough for deep folding)
sys.setrecursionlimit(10000)

# Main application class
class DataFoldingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Folding and Unfolding Tool")
        self.root.geometry("600x400")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.file_label = tk.Label(self.root, text="Select a file to fold/unfold:")
        self.file_label.pack(pady=10)

        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(self.root, textvariable=self.file_path, width=50)
        self.file_entry.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Mode selection
        self.mode_label = tk.Label(self.root, text="Select mode:")
        self.mode_label.pack(pady=10)

        self.mode_var = tk.StringVar(value="fold")
        self.fold_radio = tk.Radiobutton(self.root, text="Fold", variable=self.mode_var, value="fold")
        self.fold_radio.pack()

        self.unfold_radio = tk.Radiobutton(self.root, text="Unfold", variable=self.mode_var, value="unfold")
        self.unfold_radio.pack()

        # Execute button
        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute)
        self.execute_button.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)

    def execute(self):
        file_path = self.file_path.get()
        mode = self.mode_var.get()

        if not file_path:
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        if mode == "fold":
            self.fold_data(file_path)
        elif mode == "unfold":
            self.unfold_data(file_path)

    def fold_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = file.read()

            # Convert data to binary string
            binary_data = ''.join(format(ord(char), '08b') for char in data)

            # Fold the binary data
            folded_data = self.fold(binary_data, depth=3, max_depth=100)

            # Save folded data to a new file
            folded_file_path = file_path + ".folded"
            with open(folded_file_path, "w") as folded_file:
                folded_file.write(folded_data)

            self.status_label.config(text=f"Folding complete. Folded data saved to {folded_file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def unfold_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                folded_data = file.read()

            # Unfold the binary data
            unfolded_data = self.unfold(folded_data, depth=3, max_depth=100)

            # Convert binary data back to text
            unfolded_text = ''.join(chr(int(unfolded_data[i:i+8], 2)) for i in range(0, len(unfolded_data), 8))

            # Save unfolded data to a new file
            unfolded_file_path = file_path + ".unfolded"
            with open(unfolded_file_path, "w") as unfolded_file:
                unfolded_file.write(unfolded_text)

            self.status_label.config(text=f"Unfolding complete. Unfolded data saved to {unfolded_file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fold(self, data, depth=3, max_depth=100):
        if depth > max_depth:
            return '0' * 8  # Base case

        total_len = len(data)
        d3_time = bin(total_len)[2:].zfill(8)

        total_ones = data.count('1')
        avg_prob = total_ones / (total_len or 1)
        d4_density = bin(int(avg_prob * 255))[2:].zfill(8)

        gravity = sum(int(data[i:i+8], 2) for i in range(0, len(data), 8)) % 256
        d5_gravity = bin(gravity)[2:].zfill(8)

        payload = data[:int(len(data) * 0.5)]  # Simplified payload handling

        next_layer = self.fold(payload, depth + 1, max_depth)
        folded = d3_time + d4_density + d5_gravity + payload + next_layer

        return folded

    def unfold(self, folded_data, depth=3, max_depth=100):
        if depth > max_depth:
            return ''  # Base case

        d3_time = folded_data[:8]
        d4_density = folded_data[8:16]
        d5_gravity = folded_data[16:24]

        payload = folded_data[24:]

        next_layer = self.unfold(payload, depth + 1, max_depth)

        return next_layer + payload

if __name__ == "__main__":
    root = tk.Tk()
    app = DataFoldingApp(root)
    root.mainloop()
