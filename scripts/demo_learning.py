"""Run with python -m scripts.demo_learning. No changes to the user's persistent memory."""
import json
import tempfile
from pathlib import Path
import pandas as pd
from cognitive.memory import Memory
from cognitive.pipeline import evaluate
from cognitive.action import act
from cognitive.learning import learn

ROOT = Path(__file__).resolve().parents[1]


def demonstrate():
    raw = pd.read_csv(ROOT / 'data/demo_flows.csv').iloc[1].to_dict()
    rows = []
    with tempfile.TemporaryDirectory(prefix='netguard_learning_') as folder:
        directory = Path(folder)
        memory = Memory(directory / 'memory.sqlite3')
        for n in range(5):
            cycle = evaluate(raw, memory)
            rows.append({'Verified benign outcomes': n, 'Risk': round(cycle['reasoning']['risk'], 6),
                         'Recommendation': cycle['decision']['recommendation']})
            if n < 4:
                report = act(cycle, cycle['decision']['recommendation'], True, memory, directory / 'reports')
                learn(memory, report['id'], 0)
    return rows


if __name__ == '__main__':
    print(json.dumps(demonstrate(), indent=2))
