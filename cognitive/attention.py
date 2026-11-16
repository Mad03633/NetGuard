"""T2: select salient signals; the selection directly controls reasoning."""
IMPORTANCE = {'connection_flag': .30, 'syn_errors': .30, 'connection_volume': .20,
              'service_diversity': .15, 'failed_logins': .05}


def attend(perception: dict, top_k: int = 5) -> dict:
    if top_k not in range(1, 6):
        raise ValueError('top_k must be between 1 and 5.')
    rows = [{'signal': k, 'value': v, 'importance': IMPORTANCE[k],
             'salience': v * IMPORTANCE[k]} for k, v in perception['signals'].items()]
    rows.sort(key=lambda r: (-r['salience'], r['signal']))
    selected = rows[:top_k]
    # Keep fixed weights: dropping a signal removes its contribution, without inflation.
    score = .08 + .87 * sum(r['salience'] for r in selected)
    return {'selected': selected, 'suppressed': rows[top_k:], 'signal_risk': score,
            'pattern': perception['pattern'], 'record': perception['record']}
