from cognitive.localization import ru, table_ru, error_ru, explanation_ru
from cognitive.pipeline import evaluate
from tests.test_streamlit import app


def test_russian_labels_preserve_model_data(raw, memory):
    cycle = evaluate(raw, memory)
    original = cycle['decision']['matrix']
    localized = table_ru(original)
    assert list(original.columns) == ['Protection', 'Disruption', 'Effort']
    assert list(localized.columns) == ['Защита', 'Нарушение работы', 'Трудозатраты']
    assert localized.loc['Наблюдение', 'Защита'] == original.loc['Monitor', 'Protection']
    assert 'Предложение карантина' in explanation_ru(cycle['decision'])
    assert 'Число соединений' in error_ru(ValueError('count must be finite.')) or 'Соединения с хостом' in error_ru(ValueError('count must be finite.'))


def test_russian_ui_and_editable_matrix(monkeypatch, tmp_path):
    import hashlib
    at = app(monkeypatch, tmp_path)
    assert not at.exception
    assert at.tabs[0].label == '1 Восприятие'
    assert at.slider(key='weight_Protection').label == 'Защита · выгода'
    assert at.success[0].value.startswith('Рекомендуется: Предложение карантина')
    cycle = at.session_state['current_cycle']
    version = hashlib.sha256(repr((cycle['perception']['record'], 5, 0)).encode()).hexdigest()[:12]
    at.session_state['matrix_' + version] = {'edited_rows': {0: {'Защита': 99.0}}, 'added_rows': [], 'deleted_rows': []}
    at.run()
    assert not at.exception
    assert at.session_state['current_cycle']['decision']['matrix'].loc['Monitor', 'Protection'] == 99.0
