"""
Author: <Chuanyu> (skewcy@gmail.com)
__init__.py (c) 2024
Desc: description
Created:  2024-09-15T01:55:45.284Z
"""

from typing import Dict, Callable
from .operator import match_table as operator_match_table

match_table: Dict[str, Callable] = {**operator_match_table}
