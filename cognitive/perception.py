"""T1: parse and clean network tables without using ground-truth labels."""
from io import StringIO
import math
import pandas as pd

COLUMNS = (
    'duration protocol_type service flag src_bytes dst_bytes land wrong_fragment urgent hot '
    'num_failed_logins logged_in num_compromised root_shell su_attempted num_root '
    'num_file_creations num_shells num_access_files num_outbound_cmds is_host_login '
    'is_guest_login count srv_count serror_rate srv_serror_rate rerror_rate srv_rerror_rate '
    'same_srv_rate diff_srv_rate srv_diff_host_rate dst_host_count dst_host_srv_count '
    'dst_host_same_srv_rate dst_host_diff_srv_rate dst_host_same_src_port_rate '
    'dst_host_srv_diff_host_rate dst_host_serror_rate dst_host_srv_serror_rate '
    'dst_host_rerror_rate dst_host_srv_rerror_rate label difficulty'
).split()
CATEGORICAL = ['protocol_type', 'service', 'flag']
FEATURES = COLUMNS[:-2]
NUMERICAL = [c for c in FEATURES if c not in CATEGORICAL]
REQUIRED = CATEGORICAL + ['src_bytes', 'dst_bytes', 'count', 'serror_rate', 'diff_srv_rate']


def parse_table(data: bytes, nsl_kdd: bool = False) -> pd.DataFrame:
    """UTF-8 CSV (header) or NSL-KDD (43 positional columns), max 10,000 rows."""
    if len(data) > 5_000_000:
        raise ValueError('File exceeds 5 MB. Upload a smaller sample.')
    try:
        frame = pd.read_csv(StringIO(data.decode('utf-8-sig')), header=None if nsl_kdd else 0,
                            nrows=10_001)
    except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError('Expected a nonempty UTF-8 comma-separated table.') from exc
    if nsl_kdd:
        if len(frame.columns) != 43:
            raise ValueError('NSL-KDD input requires exactly 43 columns.')
        frame.columns = COLUMNS
    if frame.empty or len(frame) > 10_000:
        raise ValueError('Provide between 1 and 10,000 records.')
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(missing))
    return frame


def perceive(raw: dict) -> dict:
    """A record -> clean 41-feature record, derived signals and cleaning audit."""
    missing = [c for c in REQUIRED if c not in raw]
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(missing))
    cleaned, audit = {}, []
    for c in CATEGORICAL:
        if pd.isna(raw[c]) or not str(raw[c]).strip():
            raise ValueError(f'{c} cannot be empty.')
        value = str(raw[c]).strip()
        if len(value) > 64:
            raise ValueError(f'{c} must be at most 64 characters.')
        cleaned[c] = value.upper() if c == 'flag' else value.lower()
    for c in NUMERICAL:
        value = raw.get(c, 0)
        try:
            value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'{c} must be numeric.') from exc
        if not math.isfinite(value):
            raise ValueError(f'{c} must be finite.')
        upper = 1.0 if 'rate' in c else (1.0 if c in ['land', 'logged_in', 'root_shell', 'is_guest_login', 'is_host_login'] else 1e9)
        bounded = min(upper, max(0.0, value))
        if c not in raw:
            audit.append(f'{c}: absent, default 0 (reduced schema)')
        elif bounded != value:
            audit.append(f'{c}: {value:g} clipped to {bounded:g}')
        cleaned[c] = bounded
    signals = {
        'connection_flag': 0.0 if cleaned['flag'] == 'SF' else 1.0,
        'syn_errors': cleaned['serror_rate'],
        'connection_volume': min(cleaned['count'] / 200.0, 1.0),
        'service_diversity': cleaned['diff_srv_rate'],
        'failed_logins': min(cleaned['num_failed_logins'] / 5.0, 1.0),
    }
    return {'record': cleaned, 'signals': signals, 'audit': audit,
            'schema': '41 features; label/difficulty excluded',
            'pattern': cleaned['protocol_type'] + '/' + cleaned['service']}
