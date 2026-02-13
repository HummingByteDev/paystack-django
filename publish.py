#!/usr/bin/env python
"""
Script to build and upload the package to PyPI
Requires: twine, build
"""

import subprocess
import sys


def main():
    """Build and upload package."""
    commands = [
        ["python", "-m", "build"],
        ["python", "-m", "twine", "upload", "dist/*"],
    ]

    for cmd in commands:
        print(f"\n{'=' * 60}")
        print(f"Running: {' '.join(cmd)}")
        print('=' * 60)
        result = subprocess.run(cmd, cwd=".")
        if result.returncode != 0:
            print(f"Error running: {' '.join(cmd)}")
            sys.exit(1)

    print("\n✅ Package uploaded successfully!")


if __name__ == "__main__":
    main()
