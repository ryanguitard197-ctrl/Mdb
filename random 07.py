# mdb_folding_gui_v132.py - Optimized for Pydroid Font Scaling
import tkinter as tk
from tkinter import ttk, messagebox
import os

class MDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MDB Folding Tool v1.3.2")
        self.root.geometry("600x800") # Increased height for mobile screens

        # --- FIX FOR SQUASHED TEXT ---
        style = ttk.Style()
        # Increase rowheight to 60 (standard for Pydroid) to prevent overlapping
        style.configure("Treeview", rowheight=60) 
        # Optional: Make headers larger too
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        # -----------------------------

        self.label = tk.Label(root, text="MDB Folding Tool\nPure Geometric Folding - Lossless", font=("Arial", 12, "bold"))
        self.label.pack(pady=20)

        # Buttons - Using fill='x' to make them easier to tap on mobile
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        self.btn_fold = tk.Button(btn_frame, text="Fold File or Folder", command=self.fold_action, height=2, bg="#e1e1e1")
        self.btn_fold.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_unfold = tk.Button(btn_frame, text="Unfold .mdb File", command=self.unfold_action, height=2, bg="#e1e1e1")
        self.btn_unfold.pack(side="left", padx=5, expand=True, fill="x")

        self.status = tk.Label(root, text="Select an operation above", wraplength=550, fg="blue", font=("Arial", 10))
        self.status.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=550, mode="determinate")
        self.progress.pack(pady=10)

        # Main View Tree
        tree_label = tk.Label(root, text="File Explorer:", font=("Arial", 10, "bold"))
        tree_label.pack(anchor="w", padx=20)
        
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Type", "Size"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        
        # Set column widths to be more mobile friendly
        self.tree.column("Name", width=300)
        self.tree.column("Type", width=100)
        self.tree.column("Size", width=100)
        
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        self.base_path = "/storage/emulated/0/" if os.path.exists("/storage/emulated/0/") else os.path.expanduser("~")
        self.load_directory(self.tree, self.base_path)

        self.tree.bind("<Double-1>", lambda e: self.on_double_click(self.tree, e))

    def load_directory(self, tree, path):
        try:
            tree.delete(*tree.get_children())
            parent_dir = os.path.dirname(path)
            if path != parent_dir and path != "/":
                tree.insert("", "end", text=parent_dir, values=(".. (Up One Level)", "Folder", ""))

            items = os.listdir(path)
            items.sort()
            for item in items:
                full_path = os.path.join(path, item)
                item_type = "Folder" if os.path.isdir(full_path) else "File"
                size = f"{os.path.getsize(full_path) // 1024} KB" if item_type == "File" else "-"
                tree.insert("", "end", text=full_path, values=(item, item_type, size))
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access folder: {e}")

    def on_double_click(self, tree, event):
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        path = item['text']
        if os.path.isdir(path):
            self.load_directory(tree, path)

    def fold_action(self):
        self.open_browser("Select File or Folder to Fold")

    def unfold_action(self):
        self.open_browser("Select .mdb File to Unfold")

    def open_browser(self, title):
        browser = tk.Toplevel(self.root)
        browser.title(title)
        browser.geometry("600x700")

        instr = tk.Label(browser, text="Double-click folders to navigate.\nSelect the file/folder then tap 'SELECT'.", pady=10)
        instr.pack()

        tree = ttk.Treeview(browser, columns=("Name", "Type", "Size"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Size", text="Size")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_directory(tree, self.base_path)
        tree.bind("<Double-1>", lambda e: self.on_double_click(tree, e))

        select_btn = tk.Button(browser, text="CONFIRM SELECTION", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                               height=2, command=lambda: self.finalize_selection(tree, browser))
        select_btn.pack(pady=20, fill="x", padx=40)

    def finalize_selection(self, tree, browser):
        selected = tree.selection()
        if selected:
            path = tree.item(selected[0])['text']
            browser.destroy()
            self.process_selected(path)
        else:
            messagebox.showwarning("No Selection", "Please select a file or folder first.")

    def process_selected(self, path):
        self.update_status(f"Target: {path}")
        messagebox.showinfo("Processing", f"MDB Engine engaged for:\n{os.path.basename(path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MDBApp(root)
    root.mainloop()
