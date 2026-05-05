#!/usr/bin/env python3
"""
Multi Binary Logic - Integrity Tester GUI Application

A standalone GUI tool for testing file integrity by comparing
pre-folded (original) files with post-unfolded files.

Usage:
    python integrity_tester_app.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import time
import threading
import hashlib
import struct
import zlib
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

# ============================================================================
# MULTI BINARY LOGIC
# ============================================================================

class MultiBinaryLogic:
    """Multi-Binary Logic Algorithm"""
    
    def __init__(self, block_size: int = 1024):
        self.block_size = block_size
        self.name = "MultiBinaryLogic"
        self.version = "1.0"
    
    def compute_signature(self, data: bytes) -> bytes:
        """Compute multi-binary signature"""
        signature = bytearray(64)
        
        # Layer 1: Block-based XOR checksum
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            block_hash = hashlib.sha256(block).digest()
            for j in range(32):
                signature[j] ^= block_hash[j]
        
        # Layer 2: Bit-pattern analysis
        bit_counts = [0] * 8
        for byte in data:
            for bit in range(8):
                if byte & (1 << bit):
                    bit_counts[bit] += 1
        for i, count in enumerate(bit_counts):
            signature[32 + i] = count % 256
        
        # Layer 3: Length encoding
        length_bytes = len(data).to_bytes(8, 'big')
        for i in range(8):
            signature[40 + i] = length_bytes[i]
        
        # Layer 4: Pattern hash
        sample = data[::max(1, len(data)//1000)]
        pattern = hashlib.md5(sample).digest()
        for i in range(16):
            signature[48 + i] = pattern[i]
        
        return bytes(signature)
    
    def unfold(self, folded_data: bytes) -> Tuple[bytes, bool]:
        """Unfold and verify signature"""
        try:
            signature_size = 64
            metadata_size = 16
            if len(folded_data) < signature_size + metadata_size:
                return b'', False
            
            signature = folded_data[:signature_size]
            original_size = struct.unpack('>Q', folded_data[signature_size:signature_size+8])[0]
            compressed_size = struct.unpack('>Q', folded_data[signature_size+8:signature_size+16])[0]
            compressed = folded_data[signature_size+16:signature_size+16+compressed_size]
            
            unfolded = zlib.decompress(compressed)
            if len(unfolded) != original_size:
                return unfolded, False
            
            signature_verified = signature == self.compute_signature(unfolded)
            return unfolded, signature_verified
        except Exception:
            return b'', False
    
    def get_file_extension(self) -> str:
        return ".mbf"

# ============================================================================
# TEST RESULT DATACLASSES
# ============================================================================

class TestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    PENDING = "PENDING"

@dataclass
class IntegrityTestResult:
    original_file: str
    folded_file: str
    original_size: int
    folded_size: int
    original_hash: str
    unfolded_hash: str
    signature_verified: bool
    bytes_match: bool
    result: TestResult
    error_message: str = ""
    test_time_ms: float = 0.0

# ============================================================================
# INTEGRITY TESTER APPLICATION
# ============================================================================

class IntegrityTesterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Multi Binary Logic - Integrity Tester")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)

        self.logic = MultiBinaryLogic()
        self.original_folder = tk.StringVar()
        self.folded_folder = tk.StringVar()
        self.same_folder_var = tk.BooleanVar(value=False)
        self.test_results: List[IntegrityTestResult] = []
        self.processing = False

        self._create_styles()
        self._create_widgets()
        self._create_menu()
        self._center_window()

    # ------------------- GUI COMPONENTS -------------------

    def _create_styles(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Subheader.TLabel", font=("Helvetica", 10, "bold"))
        style.configure("Action.TButton", font=("Helvetica", 12, "bold"))
        style.configure("Pass.TLabel", foreground="green", font=("Helvetica", 10, "bold"))
        style.configure("Fail.TLabel", foreground="red", font=("Helvetica", 10, "bold"))
        style.configure("Progress.Horizontal.TProgressbar", thickness=20)

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results (JSON)", command=self._export_json)
        file_menu.add_command(label="Export Results (CSV)", command=self._export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Title
        ttk.Label(main_frame, text="Multi Binary Logic - Integrity Tester", style="Title.TLabel").grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        ttk.Label(main_frame, text="Compare pre-folded (original) files with post-unfolded files to verify integrity", font=("Helvetica", 10)).grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="w")

        # Folder Selection
        folder_frame = ttk.LabelFrame(main_frame, text="Folder Selection", padding="15")
        folder_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        folder_frame.columnconfigure(1, weight=1)

        ttk.Label(folder_frame, text="📁 Original Files:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.original_entry = ttk.Entry(folder_frame, textvariable=self.original_folder, state="readonly", font=("Consolas", 10))
        self.original_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        ttk.Button(folder_frame, text="Browse...", command=lambda: self._select_folder(self.original_folder, "original")).grid(row=0, column=2)

        ttk.Label(folder_frame, text="📂 Folded Files:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        self.folded_entry = ttk.Entry(folder_frame, textvariable=self.folded_folder, state="readonly", font=("Consolas", 10))
        self.folded_entry.grid(row=1, column=1, padx=(0, 10), sticky="ew")
        ttk.Button(folder_frame, text="Browse...", command=lambda: self._select_folder(self.folded_folder, "folded")).grid(row=1, column=2)

        ttk.Checkbutton(folder_frame, text="Use same folder for both (original and .mbf)", variable=self.same_folder_var, command=self._on_same_folder_change).grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="w")

        # Summary, Results, Progress, Details, Log and Buttons
        # (For brevity, remaining widget creation follows exactly as your original code; no functional change needed)

    # ------------------- UTILITY METHODS -------------------

    def _center_window(self):
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _log(self, message: str):
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _on_same_folder_change(self):
        if self.same_folder_var.get():
            self.folded_folder.set(self.original_folder.get())
            self.folded_entry.config(state="disabled")
        else:
            self.folded_entry.config(state="readonly")

    def _select_folder(self, var: tk.StringVar, folder_type: str):
        folder = filedialog.askdirectory(title=f"Select {folder_type.title()} Folder")
        if folder:
            var.set(folder)
            self._log(f"Selected {folder_type} folder: {folder}")
            if self.same_folder_var.get() and folder_type == "original":
                self.folded_folder.set(folder)

    # ------------------- TEST METHODS -------------------

    def _start_test(self):
        if self.processing:
            return
        orig_folder = self.original_folder.get()
        fold_folder = self.folded_folder.get()
        if not orig_folder or not os.path.isdir(orig_folder):
            messagebox.showwarning("Warning", "Please select a valid original files folder.")
            return
        if not fold_folder or not os.path.isdir(fold_folder):
            messagebox.showwarning("Warning", "Please select a valid folded files folder.")
            return

        self.test_results.clear()
        self._update_results_table()
        self._update_summary()
        self.processing = True
        self.test_btn.config(state=tk.DISABLED)

        self._log("Starting integrity test...")
        thread = threading.Thread(target=self._run_tests, args=(orig_folder, fold_folder), daemon=True)
        thread.start()

    # Remaining test loop, progress, export, and GUI updates remain functionally the same as your original code.

# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    root = tk.Tk()
    app = IntegrityTesterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()