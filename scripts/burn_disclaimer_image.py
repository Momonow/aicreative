#!/usr/bin/env python3
"""Compatibility wrapper for the campaign-specific image disclaimer renderer."""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.burn_pulaski_jones_disclaimer_image import main


if __name__ == "__main__":
    main()
