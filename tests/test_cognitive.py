import json
import numpy as np
import pandas as pd
import pytest
from cognitive.perception import perceive, parse_table
from cognitive.attention import attend
from cognitive.memory import Memory
from cognitive.pipeline import evaluate
from cognitive.action import act
from cognitive.learning import learn
from cognitive.decision import decide, sensitivity, DEFAULT_WEIGHTS
from scripts.demo_learning import demonstrate


def test_perception_cleans_and_never_uses_label(raw):
    raw.update(flag=' s0 ', service=' HTTP ', serror_rate=2, count=-2, label='normal')
    result = perceive(raw)
    assert result['record']['serror_rate'] == 1 and result['record']['count'] == 0
    assert result['pattern'] == 'tcp/http'
    assert len(result['record']) == 41 and 'label' not in result['record']
    raw['label'] = 'attack'
    assert result == perceive(raw)


@pytest.mark.parametrize('field,value', [('count', float('nan')), ('count', float('inf')),
                                         ('count', 'oops'), ('service', ''), ('flag', None)])
def test_perception_bad_values(raw, field, value):
    raw[field] = value
    with pytest.raises(ValueError):
        perceive(raw)


def test_table_schema():
    with pytest.raises(ValueError, match='Missing'):
        parse_table(b'foo,bar\n1,2')
    with pytest.raises(ValueError, match='43'):
        parse_table(b'1,2,3', True)
    with pytest.raises(ValueError):
        parse_table(b'')


def test_attention_changes_downstream(raw, memory):
    a = evaluate(raw, memory, top_k=1)
    b = evaluate(raw, memory, top_k=5)
    assert a['reasoning']['risk'] < b['reasoning']['risk']
    assert len(a['attention']['selected']) == 1


def test_wsm_known_hand_calculation():
    matrix = pd.DataFrame({'Protection': [100., 50., 0.], 'Disruption': [100., 0., 0.],
                           'Effort': [0., 100., 50.]}, index=['Monitor', 'Analyst review', 'Quarantine proposal'])
    result = decide(matrix, {'Protection': 2, 'Disruption': 1, 'Effort': 1})
    assert result['ranking'].loc['Monitor', 'Score'] == pytest.approx(.75)
    assert result['ranking'].loc['Analyst review', 'Score'] == pytest.approx(.5)
    assert result['ranking'].loc['Quarantine proposal', 'Score'] == pytest.approx(.375)
    assert result['recommendation'] == 'Monitor'
    assert sum(result['weights'].values()) == pytest.approx(1)


@pytest.mark.parametrize('weights', [dict(Protection=0, Disruption=0, Effort=0),
    dict(Protection=-1, Disruption=1, Effort=1), dict(Protection=np.nan, Disruption=1, Effort=1),
    dict(Protection=np.inf, Disruption=1, Effort=1), dict(Protection=1)])
def test_bad_weights(raw, memory, weights):
    with pytest.raises(ValueError):
        evaluate(raw, memory, weights)


@pytest.mark.parametrize('bad', [-1, 101, np.nan, np.inf])
def test_bad_matrix(raw, memory, bad):
    matrix = evaluate(raw, memory)['decision']['matrix']
    matrix.iloc[0, 0] = bad
    with pytest.raises(ValueError):
        decide(matrix, DEFAULT_WEIGHTS)


def test_ties_and_invariant_weight_scaling(raw, memory):
    matrix = evaluate(raw, memory)['decision']['matrix'] * 0
    a = decide(matrix, DEFAULT_WEIGHTS)
    b = decide(matrix, {k: v*100 for k, v in DEFAULT_WEIGHTS.items()})
    assert a['recommendation'] == 'Analyst review'
    pd.testing.assert_frame_equal(a['ranking'], b['ranking'])


def test_live_whatif_can_change_choice(raw, memory):
    matrix = evaluate(raw, memory)['decision']['matrix']
    safety = decide(matrix, dict(Protection=100, Disruption=0, Effort=0))
    continuity = decide(matrix, dict(Protection=0, Disruption=100, Effort=0))
    assert safety['recommendation'] == 'Quarantine proposal'
    assert continuity['recommendation'] == 'Monitor'
    assert len(sensitivity(matrix, DEFAULT_WEIGHTS)) == 63


def test_human_confirmation_report_and_duplicate_feedback(raw, memory, tmp_path):
    cycle = evaluate(raw, memory)
    assert not memory.reports()  # Read-only evaluation cannot silently create action history.
    with pytest.raises(ValueError, match='confirmation'):
        act(cycle, 'Monitor', False, memory, tmp_path / 'reports')
    report = act(cycle, 'Monitor', True, memory, tmp_path / 'reports')
    assert json.loads((tmp_path / 'reports' / (report['id'] + '.json')).read_text('utf-8'))['human_choice'] == 'Monitor'
    result = learn(memory, report['id'], 0)
    assert result['after_risk'] < result['before_risk']
    assert result['alpha'] == 1 and result['beta'] == 2
    with pytest.raises(ValueError, match='duplicate'):
        learn(memory, report['id'], 0)
    assert memory.retrieve(cycle['attention'])['confirmed'] == 1


def test_persistence_and_pattern_isolation(raw, memory, tmp_path):
    report = act(evaluate(raw, memory), 'Monitor', True, memory, tmp_path / 'reports')
    learn(memory, report['id'], 1)
    reopened = Memory(memory.path)
    assert evaluate(raw, reopened)['memory']['attacks'] == 1
    raw['service'] = 'ftp_data'
    assert evaluate(raw, reopened)['memory']['confirmed'] == 0


def test_learning_demonstrates_changed_behavior():
    rows = demonstrate()
    assert rows[0]['Risk'] > rows[-1]['Risk']
    assert rows[0]['Recommendation'] != rows[-1]['Recommendation']
    assert rows[-1]['Verified benign outcomes'] == 4


def test_no_learning_without_real_action(memory):
    with pytest.raises(ValueError, match='Unknown'):
        learn(memory, 'nonexistent', 0)
