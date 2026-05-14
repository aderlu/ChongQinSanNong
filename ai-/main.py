import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
for item in (str(PROJECT_ROOT), str(SRC_DIR)):
    if item not in sys.path:
        sys.path.insert(0, item)

from chicken_data_synthesis.cli import main


if __name__ == "__main__":
    main()
