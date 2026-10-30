#!/usr/bin/env python3
"""Wrapper: the checker lives in the plugin (skills/project-setup/scripts/verify.py) so tests and the shipped self-verify never drift."""
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.argv[0] = os.path.join(here, "..", "skills", "project-setup", "scripts", "verify.py")
runpy.run_path(sys.argv[0], run_name="__main__")
