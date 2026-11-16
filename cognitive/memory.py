"""T3: SQLite audit memory and retrieved human-verified pattern statistics."""
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class Memory:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY, created TEXT NOT NULL, pattern TEXT NOT NULL,
                    chosen TEXT NOT NULL, snapshot TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS feedback (
                    report_id TEXT PRIMARY KEY REFERENCES reports(id),
                    label INTEGER NOT NULL CHECK(label IN (0,1)), created TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS idx_pattern ON reports(pattern);
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def retrieve(self, attention: dict) -> dict:
        """Attention pattern -> historical actions and Beta posterior sufficient statistics."""
        with self.connect() as db:
            stats = db.execute('''SELECT COUNT(*) n, COALESCE(SUM(f.label),0) attacks
                FROM feedback f JOIN reports r ON r.id=f.report_id WHERE r.pattern=?''',
                               (attention['pattern'],)).fetchone()
            recent = [dict(r) for r in db.execute(
                'SELECT id, created, pattern, chosen FROM reports WHERE pattern=? ORDER BY rowid DESC LIMIT 5',
                (attention['pattern'],))]
            total = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
        n, attacks = int(stats['n']), int(stats['attacks'])
        return {'pattern': attention['pattern'], 'confirmed': n, 'attacks': attacks,
                'benign': n - attacks, 'alpha': 1 + attacks, 'beta': 1 + n - attacks,
                'posterior': (1 + attacks) / (2 + n), 'recent': recent, 'total_reports': total}

    def reports(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute('''SELECT r.id, r.created, r.pattern, r.chosen,
                f.label FROM reports r LEFT JOIN feedback f ON f.report_id=r.id ORDER BY r.rowid DESC LIMIT 100''')]

    def report(self, report_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM reports WHERE id=?', (report_id,)).fetchone()
        if row is None:
            raise ValueError('Unknown action report.')
        result = dict(row)
        result['snapshot'] = json.loads(result['snapshot'])
        return result
