#!/usr/bin/env python3
"""
Multi Binary Logic - Lossless Integrity Testing Framework
Tests file integrity through folding and unfolding operations
"""

import hashlib
import os
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Callable, Optional, List, Dict, Tuple
from enum import Enum
import zlib
import base64
import struct


class TestResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"


@dataclass
class IntegrityReport:
    """Report for a single file test"""
    filename: str
    file_size: int
    fold_time_ms: float
    unfold_time_ms: float
    original_hash: str
    final_hash: str
    multi_binary_match: bool
    integrity_result: TestResult
    error_message: Optional[str] = None
    fold_size: int = 0
    compression_ratio: float = 0.0


class MultiBinaryLogic:
    """
    Placeholder for your Multi Binary Logic implementation.
    Replace these methods with your actual algorithm.
    """
    
    def __init__(self, block_size: int = 1024):
        self.block_size = block_size
        self.name = "MultiBinaryLogic"
    
    def compute_signature(self, data: bytes) -> bytes:
        """
        Compute multi-binary signature of data.
        REPLACE THIS with your actual logic.
        """
        # Placeholder: XOR-based multi-block checksum
        signature = bytearray(32)
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            block_hash = hashlib.sha256(block).digest()
            for j in range(32):
                signature[j] ^= block_hash[j]
        return bytes(signature)
    
    def fold(self, data: bytes) -> bytes:
        """
        Fold operation - compress/encode data.
        REPLACE THIS with your folding logic.
        """
        # Placeholder: zlib compression with signature prepended
        compressed = zlib.compress(data, level=9)
        signature = self.compute_signature(data)
        return signature + b'::' + compressed
    
    def unfold(self, folded_data: bytes) -> Tuple[bytes, bool]:
        """
        Unfold operation - decompress/decode data.
        Returns (unfolded_data, integrity_verified)
        REPLACE THIS with your unfolding logic.
        """
        try:
            # Split signature and compressed data
            parts = folded_data.split(b'::', 1)
            if len(parts) != 2:
                return b'', False
            
            original_sig, compressed = parts
            unfolded = zlib.decompress(compressed)
            
            # Verify integrity
            computed_sig = self.compute_signature(unfolded)
            integrity_verified = original_sig == computed_sig
            
            return unfolded, integrity_verified
        except Exception as e:
            return b'', False
    
    def verify_integrity(self, original: bytes, unfolded: bytes) -> bool:
        """Verify that unfolded data matches original"""
        return original == unfolded


class IntegrityTester:
    """Main testing framework for file integrity verification"""
    
    def __init__(self, logic: Optional[MultiBinaryLogic] = None):
        self.logic = logic or MultiBinaryLogic()
        self.reports: List[IntegrityReport] = []
        
    def compute_hash(self, data: bytes) -> str:
        """Compute SHA-256 hash of data"""
        return hashlib.sha256(data).hexdigest()
    
    def test_file(self, filepath: str) -> IntegrityReport:
        """Test a single file through fold/unfold cycle"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            return IntegrityReport(
                filename=str(filepath),
                file_size=0,
                fold_time_ms=0,
                unfold_time_ms=0,
                original_hash="",
                final_hash="",
                multi_binary_match=False,
                integrity_result=TestResult.ERROR,
                error_message="File not found"
            )
        
        try:
            # Read original file
            with open(filepath, 'rb') as f:
                original_data = f.read()
            
            file_size = len(original_data)
            original_hash = self.compute_hash(original_data)
            
            # Fold operation
            fold_start = time.perf_counter()
            folded = self.logic.fold(original_data)
            fold_time = (time.perf_counter() - fold_start) * 1000
            fold_size = len(folded)
            compression_ratio = fold_size / file_size if file_size > 0 else 0
            
            # Unfold operation
            unfold_start = time.perf_counter()
            unfolded_data, multi_binary_match = self.logic.unfold(folded)
            unfold_time = (time.perf_counter() - unfold_start) * 1000
            
            # Verify integrity
            final_hash = self.compute_hash(unfolded_data)
            full_integrity = self.logic.verify_integrity(original_data, unfolded_data)
            
            if not full_integrity:
                result = TestResult.FAILED
                error_msg = "Data mismatch after unfold"
            elif not multi_binary_match:
                result = TestResult.FAILED
                error_msg = "Multi-binary signature mismatch"
            else:
                result = TestResult.PASSED
                error_msg = None
            
            return IntegrityReport(
                filename=str(filepath.name),
                file_size=file_size,
                fold_time_ms=fold_time,
                unfold_time_ms=unfold_time,
                original_hash=original_hash,
                final_hash=final_hash,
                multi_binary_match=multi_binary_match,
                integrity_result=result,
                error_message=error_msg,
                fold_size=fold_size,
                compression_ratio=compression_ratio
            )
            
        except Exception as e:
            return IntegrityReport(
                filename=str(filepath.name),
                file_size=0,
                fold_time_ms=0,
                unfold_time_ms=0,
                original_hash="",
                final_hash="",
                multi_binary_match=False,
                integrity_result=TestResult.ERROR,
                error_message=str(e)
            )
    
    def test_directory(self, directory: str, pattern: str = "*") -> List[IntegrityReport]:
        """Test all files in a directory matching pattern"""
        directory = Path(directory)
        files = list(directory.glob(pattern))
        
        print(f"Found {len(files)} files to test in {directory}")
        
        for i, filepath in enumerate(files, 1):
            if filepath.is_file():
                print(f"  Testing [{i}/{len(files)}]: {filepath.name}...", end=" ")
                report = self.test_file(str(filepath))
                self.reports.append(report)
                print(report.integrity_result.value)
        
        return self.reports
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate detailed test report"""
        if not self.reports:
            return "No tests performed."
        
        passed = sum(1 for r in self.reports if r.integrity_result == TestResult.PASSED)
        failed = sum(1 for r in self.reports if r.integrity_result == TestResult.FAILED)
        errors = sum(1 for r in self.reports if r.integrity_result == TestResult.ERROR)
        
        report_lines = [
            "=" * 70,
            "MULTI BINARY LOGIC - INTEGRITY TEST REPORT",
            "=" * 70,
            f"Total Tests: {len(self.reports)}",
            f"Passed: {passed}",
            f"Failed: {failed}",
            f"Errors: {errors}",
            f"Success Rate: {passed/len(self.reports)*100:.2f}%",
            "-" * 70,
            ""
        ]
        
        # Detailed results
        for report in self.reports:
            status_icon = "✓" if report.integrity_result == TestResult.PASSED else "✗"
            report_lines.extend([
                f"{status_icon} {report.filename}",
                f"  Size: {report.file_size:,} bytes",
                f"  Fold Size: {report.fold_size:,} bytes (ratio: {report.compression_ratio:.2%})",
                f"  Fold Time: {report.fold_time_ms:.2f}ms",
                f"  Unfold Time: {report.unfold_time_ms:.2f}ms",
                f"  Multi-Binary Match: {report.multi_binary_match}",
                f"  Original Hash: {report.original_hash[:16]}...",
                f"  Final Hash: {report.final_hash[:16]}...",
            ])
            if report.error_message:
                report_lines.append(f"  Error: {report.error_message}")
            report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Report saved to: {output_file}")
        
        return report_text
    
    def export_json(self, output_file: str):
        """Export reports to JSON format"""
        data = {
            "test_framework": "Multi Binary Logic Integrity Tester",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total": len(self.reports),
                "passed": sum(1 for r in self.reports if r.integrity_result == TestResult.PASSED),
                "failed": sum(1 for r in self.reports if r.integrity_result == TestResult.FAILED),
                "errors": sum(1 for r in self.reports if r.integrity_result == TestResult.ERROR)
            },
            "results": [asdict(r) for r in self.reports]
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"JSON report saved to: {output_file}")


def create_test_files(test_dir: str):
    """Create sample test files for demonstration"""
    Path(test_dir).mkdir(parents=True, exist_ok=True)
    
    # Text file
    with open(f"{test_dir}/test_text.txt", 'w') as f:
        f.write("Hello, this is a test file for multi binary logic integrity testing.\n" * 100)
    
    # Binary file with patterns
    with open(f"{test_dir}/test_binary.bin", 'wb') as f:
        f.write(bytes([i % 256 for i in range(10000)]))
    
    # JSON file
    with open(f"{test_dir}/test_data.json", 'w') as f:
        json.dump({"test": True, "data": list(range(1000))}, f)
    
    # Empty file
    open(f"{test_dir}/test_empty.txt", 'w').close()
    
    print(f"Test files created in: {test_dir}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Multi Binary Logic - Lossless Integrity Tester"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to test"
    )
    parser.add_argument(
        "-p", "--pattern",
        default="*",
        help="File pattern to match (default: *)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file for text report"
    )
    parser.add_argument(
        "-j", "--json",
        help="Output file for JSON report"
    )
    parser.add_argument(
        "--create-test-files",
        metavar="DIR",
        help="Create sample test files in directory"
    )
    
    args = parser.parse_args()
    
    # Create test files if requested
    if args.create_test_files:
        create_test_files(args.create_test_files)
        return
    
    # Require path for testing
    if not args.path:
        parser.print_help()
        print("\nError: Please provide a file or directory to test, or use --create-test-files")
        sys.exit(1)
    
    # Initialize tester
    logic = MultiBinaryLogic()
    tester = IntegrityTester(logic)
    
    # Run tests
    test_path = Path(args.path)
    if test_path.is_file():
        report = tester.test_file(str(test_path))
        tester.reports.append(report)
    elif test_path.is_dir():
        tester.test_directory(str(test_path), args.pattern)
    else:
        print(f"Error: Path not found: {args.path}")
        sys.exit(1)
    
    # Generate reports
    print("\n" + tester.generate_report(args.output))
    
    if args.json:
        tester.export_json(args.json)


if __name__ == "__main__":
    main()
