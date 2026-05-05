# Multi Binary Logic - GUI Applications

Two standalone GUI applications for file folding/unfolding and integrity testing.

## Applications

### 1. Fold/Unfold Tool (`fold_unfold_app.py`)

A GUI application for folding (compressing/encoding) and unfolding (decompressing/decoding) files.

#### Features
- **Fold Mode**: Compress/encode files with multi-binary signature
- **Unfold Mode**: Decompress/decode files and verify signature
- Folder selection with file browser
- Batch processing with progress tracking
- Select/deselect files individually
- Detailed logging

#### Usage

1. **Launch the application**:
   ```bash
   python fold_unfold_app.py
   ```

2. **Select Mode**:
   - Choose "FOLD Mode" to compress/encode files
   - Choose "UNFOLD Mode" to decompress/decode files

3. **Select Folder**:
   - Click "Browse..." to choose a folder containing your files
   - Or use File → Select Folder

4. **Select Files**:
   - Check/uncheck files in the list
   - Use "Select All" or "Deselect All" buttons

5. **Start Processing**:
   - Click "START FOLDING" or "START UNFOLDING"
   - Monitor progress and log output

#### Output Files

- **Folding**: Creates `.mbf` files (e.g., `file.txt` → `file.txt.mbf`)
- **Unfolding**: Removes `.mbf` extension (e.g., `file.txt.mbf` → `file.txt`)

---

### 2. Integrity Tester (`integrity_tester_app.py`)

A separate GUI application for testing file integrity by comparing original files with unfolded files.

#### Features
- Compare pre-folded (original) files with post-unfolded files
- Verify multi-binary signatures
- Byte-by-byte comparison
- Detailed test results with hashes
- Export results to JSON or CSV
- Summary statistics

#### Usage

1. **Launch the application**:
   ```bash
   python integrity_tester_app.py
   ```

2. **Select Folders**:
   - **Original Files**: Folder containing your original (pre-folded) files
   - **Folded Files**: Folder containing your `.mbf` (folded) files
   - Check "Use same folder" if both are in the same directory

3. **Start Test**:
   - Click "START INTEGRITY TEST"
   - The tool will:
     - Find each original file
     - Find its corresponding `.mbf` file
     - Unfold the `.mbf` file
     - Compare with the original
     - Verify the multi-binary signature

4. **Review Results**:
   - **✓ PASS**: File unfolded correctly and matches original
   - **✗ FAIL**: Data mismatch or signature verification failed
   - **⚠ ERROR**: Could not process file

5. **Export Results**:
   - File → Export Results (JSON) for detailed report
   - File → Export Results (CSV) for spreadsheet analysis

---

## Quick Start Workflow

### Step 1: Fold Your Files
1. Open `fold_unfold_app.py`
2. Select "FOLD Mode"
3. Browse to your folder
4. Select files to fold
5. Click "START FOLDING"

### Step 2: (Optional) Transfer Files
- Move or copy the `.mbf` files to another location
- Or keep them in the same folder

### Step 3: Unfold Your Files
1. Open `fold_unfold_app.py`
2. Select "UNFOLD Mode"
3. Browse to the folder with `.mbf` files
4. Select files to unfold
5. Click "START UNFOLDING"

### Step 4: Test Integrity
1. Open `integrity_tester_app.py`
2. Select folder with original files
3. Select folder with folded files (or check "Use same folder")
4. Click "START INTEGRITY TEST"
5. Review results and export if needed

---

## Launcher

Use `launcher.py` to easily access both applications:

```bash
python launcher.py
```

This opens a simple menu where you can choose which application to launch.

---

## Integrating Your Multi-Binary Logic

Both applications use the same `MultiBinaryLogic` class. To integrate your algorithm:

### Edit `fold_unfold_app.py` and `integrity_tester_app.py`

Replace the methods in the `MultiBinaryLogic` class:

```python
class MultiBinaryLogic:
    def compute_signature(self, data: bytes) -> bytes:
        """YOUR SIGNATURE ALGORITHM HERE"""
        # Return a signature based on your multi-binary logic
        pass
    
    def fold(self, data: bytes, progress_callback=None) -> bytes:
        """YOUR FOLD OPERATION HERE"""
        # Compress/encode data and embed signature
        pass
    
    def unfold(self, folded_data: bytes, progress_callback=None) -> Tuple[bytes, bool]:
        """YOUR UNFOLD OPERATION HERE"""
        # Decompress/decode and verify signature
        # Returns (unfolded_data, signature_verified)
        pass
    
    def get_file_extension(self) -> str:
        """Return your folded file extension"""
        return ".mbf"  # Change to your extension
```

**Important**: The logic in both files must be identical for integrity testing to work correctly.

---

## File Structure

```
.
├── fold_unfold_app.py       # Fold/Unfold GUI application
├── integrity_tester_app.py  # Integrity Tester GUI application
├── launcher.py              # Application launcher
└── APPS_README.md          # This file
```

---

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- No external dependencies required

---

## Example Session

```bash
# 1. Create test files
mkdir test_files
echo "Hello World" > test_files/hello.txt
echo "Test data" > test_files/test.txt

# 2. Launch fold/unfold tool
python fold_unfold_app.py
# - Select FOLD Mode
# - Browse to test_files
# - Select both files
# - Click START FOLDING
# Result: hello.txt.mbf, test.txt.mbf created

# 3. Launch integrity tester
python integrity_tester_app.py
# - Select original folder: test_files
# - Select folded folder: test_files
# - Check "Use same folder"
# - Click START INTEGRITY TEST
# Result: Both files should show "✓ PASS"
```

---

## Troubleshooting

### "Folded file not found" error
- Ensure the `.mbf` file exists in the selected folder
- Check that the file extension matches `get_file_extension()`

### "Signature verification failed" error
- The multi-binary logic in both apps must match exactly
- The file may have been corrupted during transfer

### "Data mismatch" error
- The fold/unfold operations may not be lossless
- Check your compression/decompression logic

### Application won't launch
- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python -c "import tkinter"`

---

## Tips

1. **Test with small files first** to verify your logic works correctly
2. **Keep original files** until you've verified integrity
3. **Use the same folder** option for quick testing
4. **Export results** for documentation or debugging
5. **Check the log** for detailed error messages

---

## Keyboard Shortcuts

### Fold/Unfold Tool
- `Ctrl+O` - Select Folder
- `Ctrl+A` - Select All Files
- `Ctrl+D` - Deselect All Files

### Integrity Tester
- `Ctrl+E` - Export Results (JSON)
- `Ctrl+Shift+E` - Export Results (CSV)
