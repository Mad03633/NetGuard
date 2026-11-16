"""T6: a real, local report and audit record after a human decision. No network control."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .decision import ALTERNATIVES


def act(cycle: dict, chosen: str, confirmed: bool, memory, output_dir) -> dict:
    if not confirmed:
        raise ValueError('Human confirmation is required before writing a report.')
    if chosen not in ALTERNATIVES:
        raise ValueError('Unsupported action.')
    report_id = uuid.uuid4().hex
    created = datetime.now(timezone.utc).isoformat()
    decision = cycle['decision']
    snapshot = {'report_id': report_id, 'created': created, 'mode': 'LOCAL_REPORT_ONLY',
                'pattern': cycle['perception']['pattern'], 'record': cycle['perception']['record'],
                'attention_top_k': len(cycle['attention']['selected']),
                'reasoning': cycle['reasoning'], 'memory': cycle['memory'],
                'recommendation': decision['recommendation'], 'human_choice': chosen,
                'weights': decision['weights'], 'matrix': decision['matrix'].reset_index().to_dict('records'),
                'ranking': decision['ranking'].reset_index().to_dict('records'),
                'explanation': decision['explanation'],
                'effect': 'Saved report only. No firewall changes, notifications or external calls.'}
    content = json.dumps(snapshot, ensure_ascii=False, indent=2, allow_nan=False)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    target = output / f'{report_id}.json'
    # Write first; on a database error remove only this new file.
    target.write_text(content, encoding='utf-8')
    try:
        with memory.connect() as db:
            db.execute('INSERT INTO reports VALUES (?,?,?,?,?)',
                       (report_id, created, snapshot['pattern'], chosen, content))
    except Exception:
        target.unlink(missing_ok=True)
        raise
    return {'id': report_id, 'path': str(target), 'content': content, 'snapshot': snapshot,
            'chosen': chosen, 'mode': 'LOCAL_REPORT_ONLY'}
