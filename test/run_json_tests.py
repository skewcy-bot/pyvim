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
    
    def run_test(self, test: Dict[str, Any]) -> bool:
        name = test.get('name', 'Unnamed test')
        input_text = test.get('input', '')
        commands = test.get('commands', '')
        cursor = test.get('cursor', [0, 0])
        
        if self.verbose:
            print(f"  Running: {name}")
        
        try:
            vim_result = self.vim_executor.execute_commands(
                input_text, commands, cursor[0], cursor[1]
            )
            
            if not vim_result['success']:
                self.failed += 1
                self.failures.append({
                    'test': name,
                    'error': f"Vim failed: {vim_result['vim_error']}"
                })
                if self.verbose:
                    print(f"    ✗ Vim execution failed")
                return False
            
            pyvim = VimEmulator(input_text, cursor[0], cursor[1], {"verbose": False})
            pyvim_success, _ = pyvim.exec(commands)
            
            if not pyvim_success:
                self.failed += 1
                self.failures.append({
                    'test': name,
                    'error': "PyVim execution failed"
                })
                if self.verbose:
                    print(f"    ✗ PyVim execution failed")
                return False
            
            pyvim_result = {
                'text': str(pyvim._buffer),
                'cursor_row': pyvim.row,
                'cursor_col': pyvim.col
            }
            
            text_match = vim_result['final_state']['text'] == pyvim_result['text']
            row_match = vim_result['final_state']['cursor_row'] == pyvim_result['cursor_row']
            col_match = vim_result['final_state']['cursor_col'] == pyvim_result['cursor_col']
            
            if text_match and row_match and col_match:
                self.passed += 1
                if self.verbose:
                    print(f"    ✓ Pass")
                return True
            else:
                self.failed += 1
                error_parts = []
                if not text_match:
                    error_parts.append(f"Text mismatch: vim='{vim_result['final_state']['text']}', pyvim='{pyvim_result['text']}'")
                if not row_match:
                    error_parts.append(f"Row mismatch: vim={vim_result['final_state']['cursor_row']}, pyvim={pyvim_result['cursor_row']}")
                if not col_match:
                    error_parts.append(f"Col mismatch: vim={vim_result['final_state']['cursor_col']}, pyvim={pyvim_result['cursor_col']}")
                
                self.failures.append({
                    'test': name,
                    'error': '; '.join(error_parts)
                })
                if self.verbose:
                    print(f"    ✗ {'; '.join(error_parts)}")
                return False
                
        except Exception as e:
            self.failed += 1
            self.failures.append({
                'test': name,
                'error': str(e)
            })
            if self.verbose:
                print(f"    ✗ Exception: {e}")
            return False
    
    def run_file(self, filepath: str) -> None:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        suite_name = data.get('name', Path(filepath).stem)
        tests = data.get('tests', [])
        
        print(f"\n{suite_name} ({len(tests)} tests)")
        print("-" * 50)
        
        for test in tests:
            self.run_test(test)
    
    def run_directory(self, directory: str) -> None:
        test_files = sorted(glob.glob(os.path.join(directory, '*.json')))
        
        for filepath in test_files:
            self.run_file(filepath)
    
    def print_summary(self) -> None:
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