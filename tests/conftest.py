from pathlib import Path
import pandas as pd
import pytest
from cognitive.memory import Memory

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def raw():
    return pd.read_csv(ROOT / 'data/demo_flows.csv').iloc[1].to_dict()


@pytest.fixture
def memory(tmp_path):
    return Memory(tmp_path / 'memory.sqlite3')
