"""
Author: <Chuanyu> (skewcy@gmail.com)
__init__.py (c) 2024
Desc: description
Created:  2024-09-15T14:50:54.082Z
"""

from typing import Dict, Callable

from .operator import match_table as operator_match_table

match_table: Dict[str, Callable] = {**operator_match_table}
