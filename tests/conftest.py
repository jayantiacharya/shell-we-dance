"""
conftest.py - pytest configuration

Adds src/ to the Python path so test files can import processor.py directly,
regardless of what directory pytest is run from.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
