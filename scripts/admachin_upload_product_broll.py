#!/usr/bin/env python3
"""Compatibility wrapper for the Depo campaign product B-roll uploader."""

import runpy
from pathlib import Path

TARGET = Path(__file__).resolve().with_name("depo_admachin_upload_product_broll.py")
runpy.run_path(str(TARGET), run_name="__main__")
