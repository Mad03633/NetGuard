"""T7: online Beta-Bernoulli pattern learning from a verified action outcome."""
import sqlite3
from datetime import datetime, timezone
from .attention import attend
from .perception import perceive
from .reasoning import reason
from .decision import decide
import pandas as pd


def learn(memory, report_id: str, label: int) -> dict:
    """Action id + human attack/benign label -> persisted posterior and counterfactual."""
    if type(label) is not int or label not in (0, 1):
        raise ValueError('Outcome must be 0 (benign) or 1 (attack).')
    saved = memory.report(report_id)['snapshot']
    attention = attend(perceive(saved['record']), saved['attention_top_k'])
    # Transaction and UNIQUE(report_id) prevent duplicate feedback during UI reruns.
    with memory.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        try:
            db.execute('INSERT INTO feedback VALUES (?,?,?)',
                       (report_id, label, datetime.now(timezone.utc).isoformat()))
        except sqlite3.IntegrityError as exc:
            raise ValueError('This report already has feedback; duplicate learning was blocked.') from exc
    after_memory = memory.retrieve(attention)
    after = reason(attention, after_memory)
    before_risk = saved['reasoning']['risk']
    # Keep the human's matrix adjustments by shifting only the risk-derived protection.
    matrix = pd.DataFrame(saved['matrix']).set_index('Alternative')
    after_matrix = matrix.copy()
    after_matrix['Protection'] *= after['risk'] / before_risk
    after_matrix['Protection'] = after_matrix['Protection'].clip(0, 100)
    new_decision = decide(after_matrix, saved['weights'])
    return {'report_id': report_id, 'label': label,
            'before_risk': before_risk, 'after_risk': after['risk'],
            'before_choice': saved['recommendation'], 'after_choice': new_decision['recommendation'],
            'alpha': after_memory['alpha'], 'beta': after_memory['beta'],
            'confirmed': after_memory['confirmed'], 'posterior': after_memory['posterior'],
            'method': 'Beta(1,1) prior + verified attack/benign counts; bounded evidence blend',
            'comparison': 'Stored action vs current learned state; fixed weights and other criteria. Custom Protection scaled with risk.'}
