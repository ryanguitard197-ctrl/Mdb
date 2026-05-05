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
import sys
import json
import time
import threading
import hashlib
import struct
import zlib
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Tuple
from enum import Enum


# ============================================================================
# MULTI BINARY LOGIC (Same as fold_unfold_app.py)
# ============================================================================

class MultiBinaryLogic:
    """Multi-Binary Logic Algorithm - Must match fold_unfold_app.py"""
    
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
        pattern = hashlib.md5(data[::max(1, len(data)//1000)]).digest()
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
            
            computed_sig = self.compute_signature(unfolded)
            signature_verified = signature == computed_sig
            
            return unfolded, signature_verified
            
        except Exception as e:
            return b'', False
    
    def get_file_extension(self) -> str:
        return ".mbf"


class TestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    PENDING = "PENDING"


@dataclass
class IntegrityTestResult:
    """Result of a single integrity test"""
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
    """Main GUI Application for Testing File Integrity"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Multi Binary Logic - Integrity Tester")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Initialize logic
        self.logic = MultiBinaryLogic()
        
        # State variables
        self.original_folder = tk.StringVar()
        self.folded_folder = tk.StringVar()
        self.test_results: List[IntegrityTestResult] = []
        self.processing = False
        
        # Build UI
        self._create_styles()
        self._create_widgets()
        self._create_menu()
        
        # Center window
        self._center_window()
    
    def _create_styles(self):
        """Create custom ttk styles"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Subheader.TLabel", font=("Helvetica", 10, "bold"))
        style.configure("Action.TButton", font=("Helvetica", 12, "bold"))
        style.configure("Pass.TLabel", foreground="green", font=("Helvetica", 10, "bold"))
        style.configure("Fail.TLabel", foreground="red", font=("Helvetica", 10, "bold"))
        style.configure("Progress.Horizontal.TProgressbar", thickness=20)
    
    def _create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results (JSON)", command=self._export_json)
        file_menu.add_command(label="Export Results (CSV)", command=self._export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create main UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)  # Results table expands
        
        # ===== TITLE =====
        title_label = ttk.Label(
            main_frame,
            text="Multi Binary Logic - Integrity Tester",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        subtitle = ttk.Label(
            main_frame,
            text="Compare pre-folded (original) files with post-unfolded files to verify integrity",
            font=("Helvetica", 10)
        )
        subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="w")
        
        # ===== FOLDER SELECTION =====
        folder_frame = ttk.LabelFrame(main_frame, text="Folder Selection", padding="15")
        folder_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        folder_frame.columnconfigure(1, weight=1)
        
        # Original folder
        ttk.Label(folder_frame, text="📁 Original Files:", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, padx=(0, 10), pady=5, sticky="w"
        )
        
        self.original_entry = ttk.Entry(
            folder_frame,
            textvariable=self.original_folder,
            state="readonly",
            font=("Consolas", 10)
        )
        self.original_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        
        ttk.Button(
            folder_frame,
            text="Browse...",
            command=lambda: self._select_folder(self.original_folder, "original")
        ).grid(row=0, column=2)
        
        # Folded folder
        ttk.Label(folder_frame, text="📂 Folded Files:", font=("Helvetica", 10, "bold")).grid(
            row=1, column=0, padx=(0, 10), pady=5, sticky="w"
        )
        
        self.folded_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folded_folder,
            state="readonly",
            font=("Consolas", 10)
        )
        self.folded_entry.grid(row=1, column=1, padx=(0, 10), sticky="ew")
        
        ttk.Button(
            folder_frame,
            text="Browse...",
            command=lambda: self._select_folder(self.folded_folder, "folded")
        ).grid(row=1, column=2)
        
        # Same folder checkbox
        self.same_folder_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            folder_frame,
            text="Use same folder for both (original files and .mbf files in same directory)",
            variable=self.same_folder_var,
            command=self._on_same_folder_change
        ).grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky="w")
        
        # ===== SUMMARY PANEL =====
        summary_frame = ttk.LabelFrame(main_frame, text="Test Summary", padding="15")
        summary_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        
        # Summary labels
        self.summary_total = ttk.Label(summary_frame, text="Total: 0", font=("Helvetica", 11))
        self.summary_total.grid(row=0, column=0, padx=20)
        
        self.summary_passed = ttk.Label(
            summary_frame,
            text="✓ Passed: 0",
            style="Pass.TLabel"
        )
        self.summary_passed.grid(row=0, column=1, padx=20)
        
        self.summary_failed = ttk.Label(
            summary_frame,
            text="✗ Failed: 0",
            style="Fail.TLabel"
        )
        self.summary_failed.grid(row=0, column=2, padx=20)
        
        self.summary_errors = ttk.Label(summary_frame, text="⚠ Errors: 0", foreground="orange")
        self.summary_errors.grid(row=0, column=3, padx=20)
        
        self.summary_success_rate = ttk.Label(
            summary_frame,
            text="Success Rate: 0%",
            font=("Helvetica", 11, "bold")
        )
        self.summary_success_rate.grid(row=0, column=4, padx=20)
        
        # ===== RESULTS TABLE =====
        results_frame = ttk.LabelFrame(main_frame, text="Test Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, pady=(0, 15), sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for results
        columns = (
            "status", "original", "folded", "orig_size", "fold_size",
            "orig_hash", "unfold_hash", "sig_ok", "bytes_ok"
        )
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.results_tree.heading("status", text="Status")
        self.results_tree.heading("original", text="Original File")
        self.results_tree.heading("folded", text="Folded File")
        self.results_tree.heading("orig_size", text="Orig Size")
        self.results_tree.heading("fold_size", text="Fold Size")
        self.results_tree.heading("orig_hash", text="Orig Hash")
        self.results_tree.heading("unfold_hash", text="Unfold Hash")
        self.results_tree.heading("sig_ok", text="Sig OK")
        self.results_tree.heading("bytes_ok", text="Bytes OK")
        
        self.results_tree.column("status", width=80, anchor="center")
        self.results_tree.column("original", width=200)
        self.results_tree.column("folded", width=200)
        self.results_tree.column("orig_size", width=80)
        self.results_tree.column("fold_size", width=80)
        self.results_tree.column("orig_hash", width=120)
        self.results_tree.column("unfold_hash", width=120)
        self.results_tree.column("sig_ok", width=60, anchor="center")
        self.results_tree.column("bytes_ok", width=60, anchor="center")
        
        # Scrollbar
        vsb = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_select)
        
        # ===== PROGRESS =====
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate"
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky="w")
        
        self.progress_text = ttk.Label(progress_frame, text="0%")
        self.progress_text.grid(row=1, column=1, sticky="e")
        
        # ===== DETAILS PANEL =====
        details_frame = ttk.LabelFrame(main_frame, text="Details", padding="10")
        details_frame.grid(row=6, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        details_frame.columnconfigure(0, weight=1)
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            height=6,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.details_text.grid(row=0, column=0, sticky="ew")
        
        # ===== LOG =====
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, pady=(0, 15), sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=5,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.config(state=tk.DISABLED)
        
        # ===== ACTION BUTTONS =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        self.test_btn = ttk.Button(
            button_frame,
            text="▶ START INTEGRITY TEST",
            command=self._start_test,
            style="Action.TButton"
        )
        self.test_btn.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Clear Results",
            command=self._clear_results
        ).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self._clear_log
        ).grid(row=0, column=2)
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _log(self, message: str):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _clear_log(self):
        """Clear the log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _on_same_folder_change(self):
        """Handle same folder checkbox change"""
        if self.same_folder_var.get():
            self.folded_folder.set(self.original_folder.get())
            self.folded_entry.config(state="disabled")
        else:
            self.folded_entry.config(state="readonly")
    
    def _select_folder(self, var: tk.StringVar, folder_type: str):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title=f"Select {folder_type.title()} Folder")
        if folder:
            var.set(folder)
            self._log(f"Selected {folder_type} folder: {folder}")
            
            if self.same_folder_var.get() and folder_type == "original":
                self.folded_folder.set(folder)
    
    def _format_size(self, size: int) -> str:
        """Format file size for display"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def _format_hash(self, hash_str: str) -> str:
        """Format hash for display"""
        return hash_str[:16] + "..." if len(hash_str) > 16 else hash_str
    
    def _update_summary(self):
        """Update summary panel"""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.result == TestResult.PASSED)
        failed = sum(1 for r in self.test_results if r.result == TestResult.FAILED)
        errors = sum(1 for r in self.test_results if r.result == TestResult.ERROR)
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        self.summary_total.config(text=f"Total: {total}")
        self.summary_passed.config(text=f"✓ Passed: {passed}")
        self.summary_failed.config(text=f"✗ Failed: {failed}")
        self.summary_errors.config(text=f"⚠ Errors: {errors}")
        self.summary_success_rate.config(text=f"Success Rate: {success_rate:.1f}%")
    
    def _update_results_table(self):
        """Update results table"""
        # Clear existing
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add results
        for result in self.test_results:
            # Status icon
            if result.result == TestResult.PASSED:
                status = "✓ PASS"
                tags = ("pass",)
            elif result.result == TestResult.FAILED:
                status = "✗ FAIL"
                tags = ("fail",)
            elif result.result == TestResult.ERROR:
                status = "⚠ ERROR"
                tags = ("error",)
            else:
                status = "⏳ PENDING"
                tags = ()
            
            self.results_tree.insert(
                "",
                tk.END,
                values=(
                    status,
                    result.original_file,
                    result.folded_file,
                    self._format_size(result.original_size),
                    self._format_size(result.folded_size),
                    self._format_hash(result.original_hash),
                    self._format_hash(result.unfolded_hash),
                    "✓" if result.signature_verified else "✗",
                    "✓" if result.bytes_match else "✗"
                ),
                tags=tags
            )
        
        # Configure tags
        self.results_tree.tag_configure("pass", foreground="green")
        self.results_tree.tag_configure("fail", foreground="red")
        self.results_tree.tag_configure("error", foreground="orange")
    
    def _on_result_select(self, event):
        """Handle result selection"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        idx = self.results_tree.index(selection[0])
        result = self.test_results[idx]
        
        # Show details
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = f"""Original File: {result.original_file}
Folded File: {result.folded_file}
Original Size: {self._format_size(result.original_size)}
Folded Size: {self._format_size(result.folded_size)}
Original Hash (SHA-256): {result.original_hash}
Unfolded Hash (SHA-256): {result.unfolded_hash}
Signature Verified: {'Yes' if result.signature_verified else 'No'}
Bytes Match: {'Yes' if result.bytes_match else 'No'}
Test Time: {result.test_time_ms:.2f} ms
"""
        if result.error_message:
            details += f"\nError: {result.error_message}"
        
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
    
    def _start_test(self):
        """Start integrity test"""
        if self.processing:
            return
        
        # Validate folders
        orig_folder = self.original_folder.get()
        fold_folder = self.folded_folder.get()
        
        if not orig_folder or not os.path.isdir(orig_folder):
            messagebox.showwarning("Warning", "Please select a valid original files folder.")
            return
        
        if not fold_folder or not os.path.isdir(fold_folder):
            messagebox.showwarning("Warning", "Please select a valid folded files folder.")
            return
        
        # Clear previous results
        self.test_results = []
        self._update_results_table()
        self._update_summary()
        
        # Start processing
        self.processing = True
        self.test_btn.config(state=tk.DISABLED)
        
        self._log("Starting integrity test...")
        self._log(f"Original folder: {orig_folder}")
        self._log(f"Folded folder: {fold_folder}")
        
        thread = threading.Thread(target=self._run_tests, args=(orig_folder, fold_folder))
        thread.daemon = True
        thread.start()
    
    def _run_tests(self, orig_folder: str, fold_folder: str):
        """Run integrity tests in background thread"""
        ext = self.logic.get_file_extension()
        
        # Find all original files
        original_files = []
        for filename in os.listdir(orig_folder):
            filepath = os.path.join(orig_folder, filename)
            if os.path.isfile(filepath) and not filename.endswith(ext):
                original_files.append(filename)
        
        total = len(original_files)
        self.root.after(0, self._log, f"Found {total} original files to test")
        
        for i, orig_filename in enumerate(original_files):
            progress = (i / total) * 100
            self.root.after(0, self._update_progress, progress, f"Testing {orig_filename}...")
            
            # Find corresponding folded file
            folded_filename = orig_filename + ext
            folded_path = os.path.join(fold_folder, folded_filename)
            
            if not os.path.exists(folded_path):
                # Try same folder
                folded_path = os.path.join(orig_folder, folded_filename)
            
            orig_path = os.path.join(orig_folder, orig_filename)
            
            # Run test
            result = self._test_file_pair(orig_filename, orig_path, folded_filename, folded_path)
            self.test_results.append(result)
            
            # Update UI
            self.root.after(0, self._update_results_table)
            self.root.after(0, self._update_summary)
            
            # Log result
            status = "PASS" if result.result == TestResult.PASSED else "FAIL"
            self.root.after(0, self._log, f"  {orig_filename}: {status}")
        
        # Complete
        self.root.after(0, self._update_progress, 100, "Complete")
        self.root.after(0, self._log, "Integrity test complete!")
        self.root.after(0, self._testing_complete)
    
    def _test_file_pair(self, orig_filename: str, orig_path: str, 
                        folded_filename: str, folded_path: str) -> IntegrityTestResult:
        """Test a single file pair"""
        start_time = time.perf_counter()
        
        try:
            # Check if folded file exists
            if not os.path.exists(folded_path):
                return IntegrityTestResult(
                    original_file=orig_filename,
                    folded_file=folded_filename,
                    original_size=0,
                    folded_size=0,
                    original_hash="",
                    unfolded_hash="",
                    signature_verified=False,
                    bytes_match=False,
                    result=TestResult.ERROR,
                    error_message="Folded file not found",
                    test_time_ms=0
                )
            
            # Read original file
            with open(orig_path, 'rb') as f:
                original_data = f.read()
            
            original_size = len(original_data)
            original_hash = hashlib.sha256(original_data).hexdigest()
            
            # Read folded file
            with open(folded_path, 'rb') as f:
                folded_data = f.read()
            
            folded_size = len(folded_data)
            
            # Unfold
            unfolded_data, signature_verified = self.logic.unfold(folded_data)
            
            # Compare
            bytes_match = (original_data == unfolded_data)
            unfolded_hash = hashlib.sha256(unfolded_data).hexdigest()
            
            # Determine result
            if bytes_match and signature_verified:
                result = TestResult.PASSED
                error_msg = ""
            elif not bytes_match:
                result = TestResult.FAILED
                error_msg = "Data mismatch"
            else:
                result = TestResult.FAILED
                error_msg = "Signature verification failed"
            
            test_time = (time.perf_counter() - start_time) * 1000
            
            return IntegrityTestResult(
                original_file=orig_filename,
                folded_file=folded_filename,
                original_size=original_size,
                folded_size=folded_size,
                original_hash=original_hash,
                unfolded_hash=unfolded_hash,
                signature_verified=signature_verified,
                bytes_match=bytes_match,
                result=result,
                error_message=error_msg,
                test_time_ms=test_time
            )
            
        except Exception as e:
            test_time = (time.perf_counter() - start_time) * 1000
            return IntegrityTestResult(
                original_file=orig_filename,
                folded_file=folded_filename,
                original_size=0,
                folded_size=0,
                original_hash="",
                unfolded_hash="",
                signature_verified=False,
                bytes_match=False,
                result=TestResult.ERROR,
                error_message=str(e),
                test_time_ms=test_time
            )
    
    def _update_progress(self, value: float, message: str):
        """Update progress bar"""
        self.progress_var.set(value)
        self.status_label.config(text=message)
        self.progress_text.config(text=f"{value:.0f}%")
    
    def _testing_complete(self):
        """Reset UI after testing"""
        self.processing = False
        self.test_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Ready")
        
        # Show summary
        passed = sum(1 for r in self.test_results if r.result == TestResult.PASSED)
        total = len(self.test_results)
        messagebox.showinfo("Test Complete", f"Testing complete!\n\nPassed: {passed}/{total}")
    
    def _clear_results(self):
        """Clear all results"""
        self.test_results = []
        self._update_results_table()
        self._update_summary()
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)
        self._log("Results cleared")
    
    def _export_json(self):
        """Export results to JSON"""
        if not self.test_results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Results as JSON"
        )
        
        if filepath:
            data = {
                "test_framework": "Multi Binary Logic Integrity Tester",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "summary": {
                    "total": len(self.test_results),
                    "passed": sum(1 for r in self.test_results if r.result == TestResult.PASSED),
                    "failed": sum(1 for r in self.test_results if r.result == TestResult.FAILED),
                    "errors": sum(1 for r in self.test_results if r.result == TestResult.ERROR)
                },
                "results": [
                    {
                        "original_file": r.original_file,
                        "folded_file": r.folded_file,
                        "original_size": r.original_size,
                        "folded_size": r.folded_size,
                        "original_hash": r.original_hash,
                        "unfolded_hash": r.unfolded_hash,
                        "signature_verified": r.signature_verified,
                        "bytes_match": r.bytes_match,
                        "result": r.result.value,
                        "error_message": r.error_message,
                        "test_time_ms": r.test_time_ms
                    }
                    for r in self.test_results
                ]
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            self._log(f"Results exported to: {filepath}")
            messagebox.showinfo("Export Complete", f"Results exported to:\n{filepath}")
    
    def _export_csv(self):
        """Export results to CSV"""
        if not self.test_results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Results as CSV"
        )
        
        if filepath:
            import csv
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Original File", "Folded File", "Original Size", "Folded Size",
                    "Original Hash", "Unfolded Hash", "Signature Verified",
                    "Bytes Match", "Result", "Error Message", "Test Time (ms)"
                ])
                
                for r in self.test_results:
                    writer.writerow([
                        r.original_file, r.folded_file, r.original_size, r.folded_size,
                        r.original_hash, r.unfolded_hash, r.signature_verified,
                        r.bytes_match, r.result.value, r.error_message, r.test_time_ms
                    ])
            
            self._log(f"Results exported to: {filepath}")
            messagebox.showinfo("Export Complete", f"Results exported to:\n{filepath}")
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """How to Use the Integrity Tester

1. Select Folders:
   - Choose the folder containing your ORIGINAL (pre-folded) files
   - Choose the folder containing your FOLDED (.mbf) files
   - Or check "Use same folder" if both are in the same directory

2. Start Test:
   - Click "START INTEGRITY TEST"
   - The tool will:
     a. Find each original file
     b. Find its corresponding folded file (.mbf)
     c. Unfold the folded file
     d. Compare the unfolded data with the original
     e. Verify the multi-binary signature

3. Review Results:
   - PASS: File unfolded correctly and matches original
   - FAIL: Data mismatch or signature verification failed
   - ERROR: Could not process file

4. Export Results:
   - File → Export Results (JSON) for detailed report
   - File → Export Results (CSV) for spreadsheet analysis
"""
        messagebox.showinfo("How to Use", help_text)
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            f"Multi Binary Logic - Integrity Tester\n"
            f"Version 1.0\n\n"
            f"Logic: {self.logic.name}\n"
            f"Block Size: {self.logic.block_size} bytes\n\n"
            f"A tool for testing file integrity by comparing\n"
            f"pre-folded (original) files with post-unfolded files."
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = IntegrityTesterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
