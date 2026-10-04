#!/usr/bin/env python3
"""Compatibility entry; implementation is owned by xcode-build-benchmark."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[2] / "xcode-build-benchmark/scripts/benchmark_builds.py"), run_name="__main__")
