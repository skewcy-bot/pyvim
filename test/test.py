#!/usr/bin/env python3
import sys
import os
import json
import glob
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyvim.pyvim import VimEmulator
from vim_executor import VimExecutor


class JsonTestRunner:
    def __init__(self, verbose: bool = False):
        self.vim_executor = VimExecutor()
        self.verbose = verbose
        self.passed = 0
        self.failed = 0
        self.failures = []
    
    def run_file(self, filepath: str) -> None:
        """Run all tests in a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        suite_name = data.get('name', Path(filepath).stem)
        tests = data.get('tests', [])
        
        print(f"\n{suite_name} ({len(tests)} tests)")
        print("-" * 50)
        
        if not tests:
            return
        
        # Always use batch execution for optimal performance
        try:
            vim_results = self.vim_executor.execute_batch(tests)
            for i, test in enumerate(tests):
                if i < len(vim_results):
                    self._process_test_result(test, vim_results[i])
        except Exception as e:
            if self.verbose:
                print(f"  Batch execution failed: {e}")
            # Mark all tests as failed if batch execution fails
            for test in tests:
                self._record_failure(test.get('name', 'Unnamed test'), str(e))
    
    def _process_test_result(self, test: Dict[str, Any], vim_result: Dict[str, Any]) -> None:
        """Process a single test result"""
        name = test.get('name', 'Unnamed test')
        input_text = test.get('input', '')
        commands = test.get('commands', '')
        cursor = test.get('cursor', [0, 0])
        
        if self.verbose:
            print(f"  Running: {name}")
        
        try:
            # Check vim execution
            if not vim_result['success']:
                self._record_failure(name, f"Vim failed: {vim_result['vim_error']}")
                return
            
            # Run PyVim for comparison
            pyvim = VimEmulator(input_text, cursor[0], cursor[1], {"verbose": False, "sleep_time": 0})
            pyvim_success, _ = pyvim.exec(commands)
            
            if not pyvim_success:
                self._record_failure(name, "PyVim execution failed")
                return
            
            # Compare results
            pyvim_result = {
                'text': str(pyvim._buffer),
                'cursor_row': pyvim.row,
                'cursor_col': pyvim.col
            }
            
            vim_final = vim_result['final_state']
            text_match = vim_final['text'] == pyvim_result['text']
            row_match = vim_final['cursor_row'] == pyvim_result['cursor_row']
            col_match = vim_final['cursor_col'] == pyvim_result['cursor_col']
            
            if text_match and row_match and col_match:
                self.passed += 1
                if self.verbose:
                    print(f"    ✓ Pass")
            else:
                # Build detailed error message
                errors = []
                if not text_match:
                    errors.append(f"Text mismatch: vim='{vim_final['text']}', pyvim='{pyvim_result['text']}'")
                if not row_match:
                    errors.append(f"Row mismatch: vim={vim_final['cursor_row']}, pyvim={pyvim_result['cursor_row']}")
                if not col_match:
                    errors.append(f"Col mismatch: vim={vim_final['cursor_col']}, pyvim={pyvim_result['cursor_col']}")
                
                self._record_failure(name, '; '.join(errors))
                
        except Exception as e:
            self._record_failure(name, str(e))
    
    def _record_failure(self, test_name: str, error: str) -> None:
        """Record a test failure"""
        self.failed += 1
        self.failures.append({'test': test_name, 'error': error})
        if self.verbose:
            print(f"    ✗ {error}")
    
    def run_directory(self, directory: str) -> None:
        """Run all JSON test files in a directory"""
        test_files = sorted(glob.glob(os.path.join(directory, '*.json')))
        for filepath in test_files:
            self.run_file(filepath)
    
    def print_summary(self) -> None:
        """Print test execution summary"""
        total = self.passed + self.failed
        print("\n" + "=" * 50)
        print(f"SUMMARY: {self.passed}/{total} tests passed")
        
        if self.failures:
            print(f"\nFAILURES ({len(self.failures)}):")
            for failure in self.failures:
                print(f"  • {failure['test']}: {failure['error']}")
        
        if self.failed == 0:
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ {self.failed} tests failed")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run vim tests from JSON files')
    parser.add_argument('path', nargs='?', default='test_cases',
                       help='Path to test file or directory (default: test_cases)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    args = parser.parse_args()
    
    runner = JsonTestRunner(verbose=args.verbose)
    
    if os.path.isfile(args.path):
        runner.run_file(args.path)
    elif os.path.isdir(args.path):
        runner.run_directory(args.path)
    else:
        print(f"Error: {args.path} not found")
        sys.exit(1)
    
    runner.print_summary()
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()