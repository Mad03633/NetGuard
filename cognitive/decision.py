"""T5 + D1-D5: anchored WSM, editable weights and live sensitivity."""
import numpy as np
import pandas as pd

CRITERIA = ['Protection', 'Disruption', 'Effort']
TYPES = {'Protection': 'benefit', 'Disruption': 'cost', 'Effort': 'cost'}
DEFAULT_WEIGHTS = {'Protection': .60, 'Disruption': .25, 'Effort': .15}
ALTERNATIVES = ['Monitor', 'Analyst review', 'Quarantine proposal']


def alternatives(reasoning: dict) -> pd.DataFrame:
    """Risk -> estimated 0..100 utilities/costs; assumptions, not measured effects."""
    risk = reasoning['risk']
    return pd.DataFrame({'Alternative': ALTERNATIVES,
        'Protection': [100 * risk * x for x in [.10, .65, .95]],
        'Disruption': [x * (1 - .6 * risk) for x in [1, 12, 75]],
        'Effort': [3.0, 40.0, 10.0]}).set_index('Alternative')


def decide(matrix: pd.DataFrame, weights: dict) -> dict:
    """Fixed 0..100 anchors: benefit x/100, cost 1-x/100. Weights sum to one."""
    if len(matrix) < 3 or matrix.index.has_duplicates or set(matrix.index) != set(ALTERNATIVES):
        raise ValueError('Keep the three distinct supported alternatives.')
    if set(matrix.columns) != set(CRITERIA) or set(weights) != set(CRITERIA):
        raise ValueError('Provide all three criteria and weights.')
    try:
        values = matrix[CRITERIA].astype(float)
        w = np.array([weights[c] for c in CRITERIA], dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError('Matrix and weights must be numeric.') from exc
    if not np.isfinite(values.to_numpy()).all() or ((values < 0) | (values > 100)).any().any():
        raise ValueError('Criterion values must be finite and between 0 and 100.')
    if not np.isfinite(w).all() or (w < 0).any() or w.sum() <= 0:
        raise ValueError('Weights must be finite, nonnegative and have a positive sum.')
    w /= w.sum()
    normal = values / 100
    for c in CRITERIA:
        if TYPES[c] == 'cost':
            normal[c] = 1 - normal[c]
    contributions = normal.mul(w, axis=1)
    ranking = contributions.sum(axis=1).rename('Score').to_frame()
    ranking['_alternative'] = ranking.index
    ranking = ranking.sort_values(['Score', '_alternative'], ascending=[False, True])
    ranking['Rank'] = np.arange(1, len(ranking) + 1)
    winner, runner = ranking.index[:2]
    delta = contributions.loc[winner] - contributions.loc[runner]
    driver = delta.idxmax()
    explanation = (f'{winner} leads {runner} by {ranking.loc[winner, "Score"] - ranking.loc[runner, "Score"]:.4f}. '
                   f'Largest contribution advantage: {driver} ({delta[driver]:+.4f}). '
                   'Equal scores use alphabetical order; the analyst makes the final choice.')
    return {'recommendation': winner, 'ranking': ranking.drop(columns='_alternative'),
            'normalized': normal, 'contributions': contributions,
            'weights': dict(zip(CRITERIA, w.tolist())), 'explanation': explanation,
            'matrix': values}


def sensitivity(matrix, weights):
    """Sweep protection weight; redistribute remaining weight proportionally."""
    rows = []
    other = weights['Disruption'] + weights['Effort']
    ratio = weights['Disruption'] / other if other else .5
    for protection in np.linspace(0, 1, 21):
        w = {'Protection': protection, 'Disruption': (1-protection)*ratio,
             'Effort': (1-protection)*(1-ratio)}
        result = decide(matrix, w)
        for name, row in result['ranking'].iterrows():
            rows.append({'Protection weight': protection, 'Alternative': name, 'Score': row['Score']})
    return pd.DataFrame(rows)
