from pathlib import Path;
import sys

GEN_PY_PATH = Path.home() / "AppData" / "Local" / "Temp" / "gen_py" / "3.11 ";
sys.path.append(str(GEN_PY_PATH));