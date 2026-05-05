#!/usr/bin/env python3
"""
Multi Binary Logic - Application Launcher

Launches either the Fold/Unfold tool or the Integrity Tester.

Usage:
    python launcher.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class LauncherApp:
    """Simple launcher for the two applications"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Multi Binary Logic - Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self._create_widgets()
        self._center_window()
    
    def _create_widgets(self):
        """Create launcher UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Multi Binary Logic",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(
            main_frame,
            text="File Processing & Integrity Testing Suite",
            font=("Helvetica", 12)
        )
        subtitle.pack(pady=(0, 30))
        
        # Description
        desc = ttk.Label(
            main_frame,
            text="Select an application to launch:",
            font=("Helvetica", 10)
        )
        desc.pack(pady=(0, 20))
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Fold/Unfold button
        fold_btn = ttk.Button(
            btn_frame,
            text="📁 Fold/Unfold Tool",
            command=self._launch_fold_unfold,
            width=30
        )
        fold_btn.pack(pady=10)
        
        fold_desc = ttk.Label(
            btn_frame,
            text="Fold (compress/encode) or unfold (decompress/decode) files",
            font=("Helvetica", 9),
            foreground="gray"
        )
        fold_desc.pack()
        
        # Separator
        ttk.Separator(btn_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Integrity Tester button
        test_btn = ttk.Button(
            btn_frame,
            text="🔍 Integrity Tester",
            command=self._launch_integrity_tester,
            width=30
        )
        test_btn.pack(pady=10)
        
        test_desc = ttk.Label(
            btn_frame,
            text="Test integrity by comparing original and unfolded files",
            font=("Helvetica", 9),
            foreground="gray"
        )
        test_desc.pack()
        
        # Footer
        footer = ttk.Label(
            main_frame,
            text="v1.0 - Multi Binary Logic Suite",
            font=("Helvetica", 8),
            foreground="gray"
        )
        footer.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def _center_window(self):
        """Center the window"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _launch_fold_unfold(self):
        """Launch the Fold/Unfold application"""
        script_path = os.path.join(os.path.dirname(__file__), "fold_unfold_app.py")
        if os.path.exists(script_path):
            subprocess.Popen([sys.executable, script_path])
        else:
            messagebox.showerror("Error", f"Could not find: {script_path}")
    
    def _launch_integrity_tester(self):
        """Launch the Integrity Tester application"""
        script_path = os.path.join(os.path.dirname(__file__), "integrity_tester_app.py")
        if os.path.exists(script_path):
            subprocess.Popen([sys.executable, script_path])
        else:
            messagebox.showerror("Error", f"Could not find: {script_path}")


def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
