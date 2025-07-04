#!/usr/bin/env python3
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List


class VimExecutor:
    def __init__(self, vimrc_path: str = None):
        if vimrc_path is None:
            vimrc_path = Path(__file__).parent / "vimgolf.vimrc"
        self.vimrc_path = vimrc_path
        
    def execute_batch(self, tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple tests in a single vim session for optimal performance"""
        results = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create input files for each test
            input_files = []
            for i, test in enumerate(tests):
                input_file = os.path.join(tmpdir, f"input_{i}.txt")
                with open(input_file, 'w') as f:
                    f.write(test.get('input', ''))
                input_files.append(input_file)
            
            # Create batch script
            batch_script = self._create_batch_script(tests, tmpdir, input_files)
            script_file = os.path.join(tmpdir, "batch.vim")
            with open(script_file, 'w') as f:
                f.write(batch_script)
            
            # Execute all tests in single vim session
            try:
                result = subprocess.run([
                    'vim', 
                    '-u', str(self.vimrc_path),
                    '-n', '-e', '-s',  # No swap, Ex mode, silent
                    '-c', f'source {script_file}',
                    input_files[0] if input_files else os.path.join(tmpdir, "empty.txt")
                ], capture_output=True, text=True, timeout=30)
                
                # Read results for all tests
                for i, test in enumerate(tests):
                    results.append(self._read_test_result(i, test, tmpdir, result))
                
                return results
                
            except subprocess.TimeoutExpired:
                # Return timeout results for all tests
                return [self._create_timeout_result(test) for test in tests]
    
    def _read_test_result(self, test_index: int, test: Dict[str, Any], tmpdir: str, vim_result) -> Dict[str, Any]:
        """Read result files for a specific test"""
        final_file = os.path.join(tmpdir, f"final_{test_index}.txt")
        cursor_file = os.path.join(tmpdir, f"cursor_{test_index}.txt")
        
        # Read final text
        final_text = ""
        if os.path.exists(final_file):
            with open(final_file, 'r') as f:
                final_text = f.read()
                if final_text.endswith('\n'):
                    final_text = final_text[:-1]
        
        # Read cursor position
        cursor_pos = (0, 0)
        if os.path.exists(cursor_file):
            with open(cursor_file, 'r') as f:
                cursor_data = f.read().strip().split(',')
                if len(cursor_data) == 2:
                    cursor_pos = (int(cursor_data[0]) - 1, int(cursor_data[1]) - 1)
        
        input_text = test.get('input', '')
        cursor_row = test.get('cursor', [0, 0])[0]
        cursor_col = test.get('cursor', [0, 0])[1]
        
        return {
            'initial_state': {
                'text': input_text,
                'cursor_row': cursor_row,
                'cursor_col': cursor_col
            },
            'final_state': {
                'text': final_text,
                'cursor_row': cursor_pos[0],
                'cursor_col': cursor_pos[1]
            },
            'success': vim_result.returncode == 0,
            'vim_output': vim_result.stdout,
            'vim_error': vim_result.stderr
        }
    
    def _create_timeout_result(self, test: Dict[str, Any]) -> Dict[str, Any]:
        """Create a timeout result for a test"""
        input_text = test.get('input', '')
        cursor_row = test.get('cursor', [0, 0])[0]
        cursor_col = test.get('cursor', [0, 0])[1]
        
        return {
            'initial_state': {
                'text': input_text,
                'cursor_row': cursor_row,
                'cursor_col': cursor_col
            },
            'final_state': {
                'text': input_text,
                'cursor_row': cursor_row,
                'cursor_col': cursor_col
            },
            'success': False,
            'vim_output': '',
            'vim_error': 'Timeout'
        }
    
    def _create_batch_script(self, tests: List[Dict[str, Any]], tmpdir: str, input_files: List[str]) -> str:
        """Create a vim script that executes multiple tests efficiently"""
        script_lines = []
        
        for i, test in enumerate(tests):
            commands = test.get('commands', '')
            cursor_row = test.get('cursor', [0, 0])[0]
            cursor_col = test.get('cursor', [0, 0])[1]
            
            vim_commands = self._convert_commands(commands)
            
            # Load appropriate input file and execute test
            if i == 0:
                # First test uses the buffer loaded from command line
                script_lines.append(f"""
" Test {i}
call cursor({cursor_row + 1}, {cursor_col + 1})
{vim_commands}
write! {tmpdir}/final_{i}.txt
let cursor_pos = getpos('.')
call writefile([cursor_pos[1] . ',' . cursor_pos[2]], '{tmpdir}/cursor_{i}.txt')
""")
            else:
                # Subsequent tests load their input files
                script_lines.append(f"""
" Test {i}
edit! {input_files[i]}
call cursor({cursor_row + 1}, {cursor_col + 1})
{vim_commands}
write! {tmpdir}/final_{i}.txt
let cursor_pos = getpos('.')
call writefile([cursor_pos[1] . ',' . cursor_pos[2]], '{tmpdir}/cursor_{i}.txt')
""")
        
        script_lines.append("quit!")
        return '\n'.join(script_lines)
    
    def _convert_commands(self, commands: str) -> str:
        """Convert test commands to vim script format"""
        vim_cmd = commands.replace('<Esc>', '\\<Esc>')
        vim_cmd = vim_cmd.replace('<CR>', '\\<CR>')
        vim_cmd = vim_cmd.replace('<Tab>', '\\<Tab>')
        vim_cmd = vim_cmd.replace('<BS>', '\\<BS>')
        
        return f'execute "normal! {vim_cmd}"'