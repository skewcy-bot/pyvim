#!/usr/bin/env python3
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any


class VimExecutor:
    def __init__(self, vimrc_path: str = None):
        if vimrc_path is None:
            vimrc_path = Path(__file__).parent / "vimgolf.vimrc"
        self.vimrc_path = vimrc_path
        
    def execute_commands(self, input_text: str, commands: str, 
                        cursor_row: int = 0, cursor_col: int = 0) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, 'w') as f:
                f.write(input_text)
            
            vim_script = self._create_vim_script(commands, cursor_row, cursor_col, tmpdir)
            script_file = os.path.join(tmpdir, "script.vim")
            with open(script_file, 'w') as f:
                f.write(vim_script)
            
            try:
                result = subprocess.run([
                    'vim', 
                    '-u', str(self.vimrc_path),
                    '-n',
                    '-c', f'source {script_file}',
                    input_file
                ], capture_output=True, text=True, timeout=30)
                
                final_file = os.path.join(tmpdir, "final.txt")
                cursor_file = os.path.join(tmpdir, "cursor.txt")
                
                final_text = ""
                cursor_pos = (0, 0)
                
                if os.path.exists(final_file):
                    with open(final_file, 'r') as f:
                        final_text = f.read()
                        if final_text.endswith('\n'):
                            final_text = final_text[:-1]
                
                if os.path.exists(cursor_file):
                    with open(cursor_file, 'r') as f:
                        cursor_data = f.read().strip().split(',')
                        if len(cursor_data) == 2:
                            cursor_pos = (int(cursor_data[0]) - 1, int(cursor_data[1]) - 1)
                
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
                    'success': result.returncode == 0,
                    'vim_output': result.stdout,
                    'vim_error': result.stderr
                }
                
            except subprocess.TimeoutExpired:
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
    
    def _create_vim_script(self, commands: str, cursor_row: int, cursor_col: int, tmpdir: str) -> str:
        vim_commands = self._convert_commands(commands)
        
        script = f"""
call cursor({cursor_row + 1}, {cursor_col + 1})
{vim_commands}
write! {tmpdir}/final.txt
let cursor_pos = getpos('.')
call writefile([cursor_pos[1] . ',' . cursor_pos[2]], '{tmpdir}/cursor.txt')
quit!
"""
        return script
    
    def _convert_commands(self, commands: str) -> str:
        vim_cmd = commands.replace('<Esc>', '\\<Esc>')
        vim_cmd = vim_cmd.replace('<CR>', '\\<CR>')
        vim_cmd = vim_cmd.replace('<Tab>', '\\<Tab>')
        vim_cmd = vim_cmd.replace('<BS>', '\\<BS>')
        
        return f'execute "normal! {vim_cmd}"'