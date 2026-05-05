# mdb_folding_gui_v132.py - Fixed Version
import tkinter as tk
from tkinter import ttk, messagebox
import os

class MDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MDB Folding Tool v1.3.2")
        self.root.geometry("600x600")

        self.label = tk.Label(root, text="MDB Folding Tool\nPure Geometric Folding - Lossless", font=("Arial", 10, "bold"))
        self.label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        self.btn_fold = tk.Button(btn_frame, text="Fold File or Folder", command=self.fold_action, width=25, bg="#e1e1e1")
        self.btn_fold.pack(side="left", padx=5)

        self.btn_unfold = tk.Button(btn_frame, text="Unfold .mdb File", command=self.unfold_action, width=25, bg="#e1e1e1")
        self.btn_unfold.pack(side="left", padx=5)

        self.status = tk.Label(root, text="Select an operation above", wraplength=550, fg="blue")
        self.status.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=550, mode="determinate")
        self.progress.pack(pady=5)

        # Main View Tree
        tree_label = tk.Label(root, text="File Explorer:")
        tree_label.pack(anchor="w", padx=15)
        
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Type", "Size"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Start Path
        self.base_path = "/storage/emulated/0/" if os.path.exists("/storage/emulated/0/") else os.path.expanduser("~")
        self.load_directory(self.tree, self.base_path)

        # Bindings for main tree
        self.tree.bind("<Double-1>", lambda e: self.on_double_click(self.tree, e))
        self.selected_path = None

    def update_status(self, text):
        self.status.config(text=text)
        self.root.update_idletasks()

    def load_directory(self, tree, path):
        """Clears and reloads the tree with contents of path."""
        try:
            tree.delete(*tree.get_children())
            # Add ".." to go up if not at root
            parent_dir = os.path.dirname(path)
            if path != parent_dir:
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
        browser.geometry("500(400")

        instr = tk.Label(browser, text="Double-click folders to navigate. Click 'Select' to confirm.")
        instr.pack(pady=5)

        tree = ttk.Treeview(browser, columns=("Name", "Type", "Size"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Size", text="Size")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_directory(tree, self.base_path)

        # Local bindings for the browser window
        tree.bind("<Double-1>", lambda e: self.on_double_click(tree, e))

        select_btn = tk.Button(browser, text="SELECT THIS ITEM", bg="green", fg="white", 
                               command=lambda: self.finalize_selection(tree, browser))
        select_btn.pack(pady=10)

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
        # Placeholder for MDB Logic
        self.progress['value'] = 50
        messagebox.showinfo("MDB Engine", f"Ready to process:\n{path}\n\nSHA256: [Pending]")
        self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = MDBApp(root)
    root.mainloop()
