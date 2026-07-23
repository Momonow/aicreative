#!/usr/bin/env python3
"""Compatibility wrapper for the Pulaski/Jones minimalist campaign renderer."""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.render_pulaski_jones_minimal_ad import main


if __name__ == "__main__":
    main()
