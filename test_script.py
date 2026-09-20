from typing import List
from importlib import import_module
import sys

def main():
    try:
        mod = import_module("longest-common-prefix".replace("-", "_"))
    except Exception as e:
        print("Import error:", e)
        # Attempt to run directly to check for syntax errors
        with open("longest-common-prefix.py") as f:
            code = f.read()
            exec(code)
    print("Success")

if __name__ == "__main__":
    main()
