import sys
import os

# Add src to python path for easier imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from gui.app import main

if __name__ == "__main__":
    main()
