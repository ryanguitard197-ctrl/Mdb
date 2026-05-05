#!/usr/bin/env python3
"""
Multi Binary Logic - Fold/Unfold GUI Application

A standalone GUI tool for folding and unfolding files using
custom multi-binary logic algorithms.

Usage:
    python fold_unfold_app.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import json
import time
import threading
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Callable, List, Tuple
import hashlib
import zlib
import struct


# ============================================================================
# MULTI BINARY LOGIC IMPLEMENTATION
# ============================================================================

class MultiBinaryLogic:
    """
    Multi-Binary Logic Algorithm for Folding and Unfolding
    
    INTEGRATE YOUR ALGORITHM HERE:
    - Replace compute_signature() with your signature generation
    - Replace fold() with your folding logic
    - Replace unfold() with your unfolding logic
    """
    
    def __init__(self, block_size: int = 1024):
        self.block_size = block_size
        self.name = "MultiBinaryLogic"
        self.version = "1.0"
    
    def compute_signature(self, data: bytes) -> bytes:
        """
        Compute multi-binary signature of data.
        
        YOUR SIGNATURE ALGORITHM HERE:
        This should generate a unique signature based on your multi-binary logic.
        The signature is used to verify integrity after unfolding.
        """
        # Example: Multi-layer signature (64 bytes)
        signature = bytearray(64)
        
        # Layer 1: Block-based XOR checksum (32 bytes)
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            block_hash = hashlib.sha256(block).digest()
            for j in range(32):
                signature[j] ^= block_hash[j]
        
        # Layer 2: Bit-pattern analysis (8 bytes)
        bit_counts = [0] * 8
        for byte in data:
            for bit in range(8):
                if byte & (1 << bit):
                    bit_counts[bit] += 1
        for i, count in enumerate(bit_counts):
            signature[32 + i] = count % 256
        
        # Layer 3: Length encoding (8 bytes)
        length_bytes = len(data).to_bytes(8, 'big')
        for i in range(8):
            signature[40 + i] = length_bytes[i]
        
        # Layer 4: Pattern hash (16 bytes)
        pattern = hashlib.md5(data[::max(1, len(data)//1000)]).digest()
        for i in range(16):
            signature[48 + i] = pattern[i]
        
        return bytes(signature)
    
    def fold(self, data: bytes, progress_callback: Optional[Callable[[int, int], None]] = None) -> bytes:
        """
        Fold operation - compress/encode data with signature.
        
        YOUR FOLD LOGIC HERE:
        This should compress or encode the data while embedding the signature
        for later verification.
        
        Structure: [SIGNATURE(64)][METADATA(16)][COMPRESSED_DATA]
        """
        # Compute signature
        if progress_callback:
            progress_callback(10, 100)
        
        signature = self.compute_signature(data)
        
        if progress_callback:
            progress_callback(30, 100)
        
        # Compress data (replace with your encoding)
        compressed = zlib.compress(data, level=9)
        
        if progress_callback:
            progress_callback(60, 100)
        
        # Build folded structure
        original_size = len(data)
        compressed_size = len(compressed)
        
        folded = (
            signature +
            struct.pack('>Q', original_size) +      # 8 bytes: original size
            struct.pack('>Q', compressed_size) +    # 8 bytes: compressed size
            compressed
        )
        
        if progress_callback:
            progress_callback(100, 100)
        
        return folded
    
    def unfold(self, folded_data: bytes, progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bytes, bool]:
        """
        Unfold operation - decompress/decode data and verify signature.
        
        YOUR UNFOLD LOGIC HERE:
        This should reverse the fold operation and verify the signature.
        
        Returns: (unfolded_data, signature_verified)
        """
        try:
            if progress_callback:
                progress_callback(10, 100)
            
            # Parse structure
            signature_size = 64
            metadata_size = 16
            
            if len(folded_data) < signature_size + metadata_size:
                return b'', False
            
            # Extract components
            signature = folded_data[:signature_size]
            original_size = struct.unpack('>Q', folded_data[signature_size:signature_size+8])[0]
            compressed_size = struct.unpack('>Q', folded_data[signature_size+8:signature_size+16])[0]
            compressed = folded_data[signature_size+16:signature_size+16+compressed_size]
            
            if progress_callback:
                progress_callback(40, 100)
            
            # Decompress
            unfolded = zlib.decompress(compressed)
            
            if progress_callback:
                progress_callback(70, 100)
            
            # Verify size
            if len(unfolded) != original_size:
                return unfolded, False
            
            # Verify signature
            computed_sig = self.compute_signature(unfolded)
            signature_verified = signature == computed_sig
            
            if progress_callback:
                progress_callback(100, 100)
            
            return unfolded, signature_verified
            
        except Exception as e:
            return b'', False
    
    def get_file_extension(self) -> str:
        """Return the file extension for folded files"""
        return ".mbf"  # Multi-Binary Folded


# ============================================================================
# FOLD/UNFOLD APPLICATION
# ============================================================================

class FoldUnfoldApp:
    """Main GUI Application for Folding and Unfolding Files"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Multi Binary Logic - Fold/Unfold Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize logic
        self.logic = MultiBinaryLogic()
        
        # State variables
        self.selected_folder = tk.StringVar()
        self.mode = tk.StringVar(value="fold")  # "fold" or "unfold"
        self.files = []  # List of (filename, filepath, selected)
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
        style.configure("Mode.TButton", font=("Helvetica", 11))
        style.configure("Action.TButton", font=("Helvetica", 12, "bold"))
        style.configure("Progress.Horizontal.TProgressbar", thickness=20)
    
    def _create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Folder...", command=self._select_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create main UI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # File list expands
        
        # ===== TITLE =====
        title_label = ttk.Label(
            main_frame,
            text="Multi Binary Logic - Fold/Unfold Tool",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        
        # ===== MODE SELECTION =====
        mode_frame = ttk.LabelFrame(main_frame, text="Mode Selection", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        mode_frame.columnconfigure(0, weight=1)
        mode_frame.columnconfigure(1, weight=1)
        
        self.fold_radio = ttk.Radiobutton(
            mode_frame,
            text="📁 FOLD Mode - Compress/Encode Files",
            variable=self.mode,
            value="fold",
            command=self._on_mode_change
        )
        self.fold_radio.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.unfold_radio = ttk.Radiobutton(
            mode_frame,
            text="📂 UNFOLD Mode - Decompress/Decode Files",
            variable=self.mode,
            value="unfold",
            command=self._on_mode_change
        )
        self.unfold_radio.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # ===== FOLDER SELECTION =====
        folder_frame = ttk.LabelFrame(main_frame, text="Folder Selection", padding="10")
        folder_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.selected_folder,
            state="readonly",
            font=("Consolas", 10)
        )
        self.folder_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.browse_btn = ttk.Button(
            folder_frame,
            text="Browse...",
            command=self._select_folder
        )
        self.browse_btn.grid(row=0, column=1)
        
        # ===== FILE LIST =====
        file_frame = ttk.LabelFrame(main_frame, text="Files", padding="10")
        file_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15), sticky="nsew")
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(1, weight=1)
        
        # File list toolbar
        toolbar = ttk.Frame(file_frame)
        toolbar.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        
        ttk.Button(toolbar, text="Select All", command=self._select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Deselect All", command=self._deselect_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self._refresh_files).pack(side=tk.LEFT)
        
        self.file_count_label = ttk.Label(toolbar, text="0 files")
        self.file_count_label.pack(side=tk.RIGHT)
        
        # File list with scrollbar
        list_container = ttk.Frame(file_frame)
        list_container.grid(row=1, column=0, columnspan=2, sticky="nsew")
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        # Treeview for files
        columns = ("select", "filename", "size", "status")
        self.file_tree = ttk.Treeview(
            list_container,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        self.file_tree.heading("select", text="☑")
        self.file_tree.heading("filename", text="Filename")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("status", text="Status")
        
        self.file_tree.column("select", width=30, anchor="center")
        self.file_tree.column("filename", width=400)
        self.file_tree.column("size", width=100)
        self.file_tree.column("status", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind click event for checkbox toggle
        self.file_tree.bind("<ButtonRelease-1>", self._on_file_click)
        
        # ===== PROGRESS =====
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, pady=(0, 15), sticky="ew")
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
            style="Progress.Horizontal.TProgressbar"
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky="w")
        
        self.progress_text = ttk.Label(progress_frame, text="0%")
        self.progress_text.grid(row=1, column=1, sticky="e")
        
        # ===== LOG =====
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, pady=(0, 15), sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.config(state=tk.DISABLED)
        
        # ===== ACTION BUTTONS =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        
        self.process_btn = ttk.Button(
            button_frame,
            text="▶ START FOLDING",
            command=self._start_processing,
            style="Action.TButton"
        )
        self.process_btn.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self._clear_log
        ).grid(row=0, column=1)
    
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
    
    def _on_mode_change(self):
        """Handle mode change"""
        mode = self.mode.get()
        if mode == "fold":
            self.process_btn.config(text="▶ START FOLDING")
        else:
            self.process_btn.config(text="▶ START UNFOLDING")
        self._refresh_files()
    
    def _select_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.selected_folder.set(folder)
            self._log(f"Selected folder: {folder}")
            self._load_files()
    
    def _load_files(self):
        """Load files from selected folder"""
        folder = self.selected_folder.get()
        if not folder or not os.path.isdir(folder):
            return
        
        self.files = []
        mode = self.mode.get()
        
        try:
            for filename in sorted(os.listdir(folder)):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    # Filter based on mode
                    if mode == "unfold":
                        # In unfold mode, only show .mbf files
                        if not filename.endswith(self.logic.get_file_extension()):
                            continue
                    
                    size = os.path.getsize(filepath)
                    size_str = self._format_size(size)
                    self.files.append({
                        "filename": filename,
                        "filepath": filepath,
                        "size": size,
                        "size_str": size_str,
                        "selected": True,
                        "status": "Pending"
                    })
            
            self._update_file_list()
            self._log(f"Loaded {len(self.files)} files")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files: {str(e)}")
            self._log(f"ERROR: Failed to load files - {str(e)}")
    
    def _format_size(self, size: int) -> str:
        """Format file size for display"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def _update_file_list(self):
        """Update the file list display"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add files
        for i, file_info in enumerate(self.files):
            checkbox = "☑" if file_info["selected"] else "☐"
            self.file_tree.insert(
                "",
                tk.END,
                iid=str(i),
                values=(
                    checkbox,
                    file_info["filename"],
                    file_info["size_str"],
                    file_info["status"]
                )
            )
        
        # Update count
        selected_count = sum(1 for f in self.files if f["selected"])
        self.file_count_label.config(text=f"{selected_count}/{len(self.files)} files")
    
    def _on_file_click(self, event):
        """Handle file list click"""
        region = self.file_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.file_tree.identify_column(event.x)
        item = self.file_tree.identify_row(event.y)
        
        if not item:
            return
        
        # Toggle checkbox if clicked on select column
        if column == "#1":  # select column
            idx = int(item)
            self.files[idx]["selected"] = not self.files[idx]["selected"]
            self._update_file_list()
    
    def _select_all(self):
        """Select all files"""
        for f in self.files:
            f["selected"] = True
        self._update_file_list()
    
    def _deselect_all(self):
        """Deselect all files"""
        for f in self.files:
            f["selected"] = False
        self._update_file_list()
    
    def _refresh_files(self):
        """Refresh the file list"""
        self._load_files()
    
    def _start_processing(self):
        """Start fold/unfold processing"""
        if self.processing:
            return
        
        # Validate
        folder = self.selected_folder.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        
        selected_files = [f for f in self.files if f["selected"]]
        if not selected_files:
            messagebox.showwarning("Warning", "Please select at least one file.")
            return
        
        # Start processing in separate thread
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.browse_btn.config(state=tk.DISABLED)
        
        mode = self.mode.get()
        self._log(f"Starting {mode} operation for {len(selected_files)} files...")
        
        thread = threading.Thread(target=self._process_files, args=(selected_files, mode))
        thread.daemon = True
        thread.start()
    
    def _process_files(self, files: List[dict], mode: str):
        """Process files in background thread"""
        total = len(files)
        success_count = 0
        fail_count = 0
        
        for i, file_info in enumerate(files):
            # Update progress
            progress = (i / total) * 100
            self.root.after(0, self._update_progress, progress, f"Processing {file_info['filename']}...")
            
            try:
                if mode == "fold":
                    result = self._fold_file(file_info)
                else:
                    result = self._unfold_file(file_info)
                
                if result:
                    success_count += 1
                    file_info["status"] = "✓ Done"
                else:
                    fail_count += 1
                    file_info["status"] = "✗ Failed"
                    
            except Exception as e:
                fail_count += 1
                file_info["status"] = f"✗ Error"
                self.root.after(0, self._log, f"ERROR processing {file_info['filename']}: {str(e)}")
            
            # Update file list
            self.root.after(0, self._update_file_list)
        
        # Complete
        self.root.after(0, self._update_progress, 100, "Complete")
        self.root.after(0, self._log, f"Processing complete. Success: {success_count}, Failed: {fail_count}")
        self.root.after(0, self._processing_complete)
    
    def _fold_file(self, file_info: dict) -> bool:
        """Fold a single file"""
        filepath = file_info["filepath"]
        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        
        # Read original file
        with open(filepath, 'rb') as f:
            data = f.read()
        
        self.root.after(0, self._log, f"Folding {filename} ({self._format_size(len(data))})...")
        
        # Fold
        folded = self.logic.fold(data)
        
        # Write folded file
        output_name = filename + self.logic.get_file_extension()
        output_path = os.path.join(folder, output_name)
        
        with open(output_path, 'wb') as f:
            f.write(folded)
        
        self.root.after(0, self._log, f"  Created: {output_name} ({self._format_size(len(folded))})")
        
        return True
    
    def _unfold_file(self, file_info: dict) -> bool:
        """Unfold a single file"""
        filepath = file_info["filepath"]
        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        
        # Read folded file
        with open(filepath, 'rb') as f:
            folded = f.read()
        
        self.root.after(0, self._log, f"Unfolding {filename} ({self._format_size(len(folded))})...")
        
        # Unfold
        unfolded, verified = self.logic.unfold(folded)
        
        if not verified:
            self.root.after(0, self._log, f"  WARNING: Signature verification failed!")
        
        # Write unfolded file
        ext = self.logic.get_file_extension()
        if filename.endswith(ext):
            output_name = filename[:-len(ext)]
        else:
            output_name = filename + ".unfolded"
        
        output_path = os.path.join(folder, output_name)
        
        with open(output_path, 'wb') as f:
            f.write(unfolded)
        
        status = "verified" if verified else "unverified"
        self.root.after(0, self._log, f"  Created: {output_name} ({self._format_size(len(unfolded))}) [{status}]")
        
        return True
    
    def _update_progress(self, value: float, message: str):
        """Update progress bar"""
        self.progress_var.set(value)
        self.status_label.config(text=message)
        self.progress_text.config(text=f"{value:.0f}%")
    
    def _processing_complete(self):
        """Reset UI after processing"""
        self.processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Ready")
        messagebox.showinfo("Complete", "Processing complete!")
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            f"Multi Binary Logic - Fold/Unfold Tool\n"
            f"Version 1.0\n\n"
            f"Logic: {self.logic.name}\n"
            f"Block Size: {self.logic.block_size} bytes\n\n"
            f"A tool for folding and unfolding files using\n"
            f"custom multi-binary logic algorithms."
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FoldUnfoldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
