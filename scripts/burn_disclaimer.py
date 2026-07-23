#!/usr/bin/env python3
"""Compatibility wrapper for the Pulaski/Jones campaign disclaimer renderer.

New work should call burn_pulaski_jones_disclaimer.py explicitly.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.burn_pulaski_jones_disclaimer import burn_disclaimer, main


if __name__ == "__main__":
    main()
