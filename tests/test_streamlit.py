from streamlit.testing.v1 import AppTest
from tests.conftest import ROOT


def app(monkeypatch, tmp_path):
    monkeypatch.setenv('NETGUARD_RUNTIME_DIR', str(tmp_path / 'runtime'))
    return AppTest.from_file(str(ROOT / 'streamlit_app.py'), default_timeout=30).run()


def test_launch_and_seven_stages(monkeypatch, tmp_path):
    at = app(monkeypatch, tmp_path)
    assert not at.exception
    assert len(at.tabs) == 8
    assert at.session_state['current_cycle']['memory']['confirmed'] == 0
    at.slider(key='top_k').set_value(1).run()
    assert not at.exception
    assert len(at.session_state['current_cycle']['attention']['selected']) == 1


def test_dss_weight_and_whatif_interaction(monkeypatch, tmp_path):
    at = app(monkeypatch, tmp_path)
    at.slider(key='whatif_Protection').set_value(0)
    at.slider(key='whatif_Disruption').set_value(100)
    at.slider(key='whatif_Effort').set_value(0).run()
    assert not at.exception
    assert at.session_state['whatif_recommendation'] == 'Monitor'
    at.slider(key='weight_Protection').set_value(0)
    at.slider(key='weight_Disruption').set_value(0)
    at.slider(key='weight_Effort').set_value(0).run()
    assert not at.exception
    assert any('больше нуля' in x.value for x in at.error)


def test_human_action_and_learning_ui(monkeypatch, tmp_path):
    at = app(monkeypatch, tmp_path)
    at.checkbox(key='confirm_action').check()
    at.button(key='save_report').click().run()
    assert not at.exception
    report = at.session_state['last_action']
    assert report['mode'] == 'LOCAL_REPORT_ONLY'
    at.button(key='apply_feedback').click().run()
    assert not at.exception
    result = at.session_state['learning_result']
    assert result['after_risk'] < result['before_risk']
    assert at.session_state['current_cycle']['memory']['confirmed'] == 1
    at.button(key='apply_feedback').click().run()
    assert any('Повторное обучение заблокировано' in w.value for w in at.warning)


def test_input_switch_and_isolated_learning(monkeypatch, tmp_path):
    at = app(monkeypatch, tmp_path)
    at.selectbox(key='scenario').set_value('normal_ftp').run()
    assert at.session_state['current_cycle']['reasoning']['level'] == 'LOW'
    at.radio(key='source').set_value('NSL-KDD test sample').run()
    assert not at.exception
    at.button(key='demo_learning').click().run()
    assert not at.exception
    assert len(at.session_state['learning_demo']) == 5
