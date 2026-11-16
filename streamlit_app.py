"""NetGuard cognitive DSS. Run: streamlit run streamlit_app.py"""
import hashlib
import json
import os
from pathlib import Path
import pandas as pd
import streamlit as st
from cognitive.perception import parse_table, COLUMNS
from cognitive.memory import Memory
from cognitive.pipeline import evaluate
from cognitive.decision import CRITERIA, TYPES, DEFAULT_WEIGHTS, decide, sensitivity
from cognitive.action import act
from cognitive.learning import learn
from cognitive.localization import ru, table_ru, view_ru, error_ru, audit_ru, explanation_ru, reasoning_ru

ROOT = Path(__file__).resolve().parent
RUNTIME = Path(os.environ.get('NETGUARD_RUNTIME_DIR', str(ROOT / 'runtime')))
st.set_page_config(page_title='NetGuard · Поддержка принятия решений', page_icon='🛡️', layout='wide')
st.title('NetGuard · Поддержка решений')
st.caption('Анализ сетевых инцидентов · Семь когнитивных функций · Решение принимает человек · Локальные отчёты')
memory = Memory(RUNTIME / 'cognitive.sqlite3')

with st.sidebar:
    st.header('Данные и приоритеты')
    source = st.radio('Источник трафика', ['Demo scenarios', 'Upload table', 'NSL-KDD test sample'], format_func=ru, key='source')
    try:
        if source == 'Demo scenarios':
            frame = pd.read_csv(ROOT / 'data/demo_flows.csv')
            selected = st.selectbox('Сценарий', frame['event_id'].tolist(), index=1, format_func=ru, key='scenario')
            raw = frame.loc[frame['event_id'] == selected].iloc[0].to_dict()
        elif source == 'Upload table':
            uploaded = st.file_uploader('Таблица CSV (UTF-8) или TXT NSL-KDD', type=['csv', 'txt'], key='upload')
            nsl = st.checkbox('43 столбца без заголовка (NSL-KDD)', key='nsl_upload')
            if uploaded is None:
                st.info('Загрузите таблицу. Шаблон CSV можно скачать во вкладке «Восприятие» в демонстрационном режиме.')
                st.stop()
            frame = parse_table(uploaded.getvalue(), nsl)
            index = st.number_input('Номер строки (с нуля)', 0, len(frame) - 1, 0, key='upload_index')
            raw = frame.iloc[int(index)].to_dict()
        else:
            frame = pd.read_csv(ROOT / 'data/KDDTest+.txt', names=COLUMNS, nrows=1000)
            index = st.number_input('Строка NSL-KDD (первые 1000)', 0, len(frame) - 1, 0, key='kdd_index')
            raw = frame.iloc[int(index)].to_dict()
    except (ValueError, OSError, pd.errors.ParserError) as exc:
        st.error(error_ru(exc))
        st.stop()
    top_k = st.slider('Внимание: число выбранных сигналов', 1, 5, 5, key='top_k')
    st.subheader('Веса критериев')
    weights = {c: st.slider(f'{ru(c)} · {ru(TYPES[c])}', 0, 100, int(DEFAULT_WEIGHTS[c]*100),
                             key=f'weight_{c}') for c in CRITERIA}
    st.caption('Веса нормируются до суммы 1. Хотя бы один вес должен быть больше нуля.')
    st.caption('Истинные метки нужны только для оценки качества и не участвуют в расчёте риска.')

try:
    cycle = evaluate(raw, memory, weights, top_k)
except ValueError as exc:
    st.error(error_ru(exc))
    st.stop()

with st.expander('Допущения СППР · редактирование оценок критериев (0–100)'):
    st.caption('Защита — ожидаемое предотвращение вреда (выгода). Нарушение работы и трудозатраты аналитика — затраты. '
               'Это явные допущения сценария, а не измеренные результаты реальных мер защиты. '
               'При изменении трафика, внимания или обученного состояния матрица формируется заново.')
    version = hashlib.sha256(repr((cycle['perception']['record'], top_k, cycle['memory']['confirmed'])).encode()).hexdigest()[:12]
    displayed = st.data_editor(table_ru(cycle['decision']['matrix']), key='matrix_' + version,
                           disabled=False, num_rows='fixed', use_container_width=True,
                           column_config={ru(c): st.column_config.NumberColumn(ru(c), min_value=0., max_value=100., format='%.2f')
                                          for c in CRITERIA})
    reverse = {ru(c): c for c in CRITERIA + list(cycle['decision']['matrix'].index)}
    matrix = displayed.rename(columns=reverse, index=reverse)
    matrix.index.name = 'Alternative'
    try:
        cycle['decision'] = decide(matrix, weights)
    except ValueError as exc:
        st.error(error_ru(exc))
        st.stop()

st.session_state['current_cycle'] = cycle
decision = cycle['decision']
c1, c2, c3, c4 = st.columns(4)
c1.metric('Индекс риска', f'{cycle["reasoning"]["risk"]:.3f}')
c2.metric('Уровень риска', ru(cycle['reasoning']['level']))
c3.metric('Подтверждённых исходов', cycle['memory']['confirmed'])
c4.metric('Протокол и сервис', cycle['perception']['pattern'])
st.success('Рекомендуется: ' + ru(decision['recommendation']))
st.write(explanation_ru(decision))

tabs = st.tabs(['1 Восприятие', '2 Внимание', '3 Память', '4 Рассуждение', '5 Решение / СППР',
                '6 Действие', '7 Обучение', 'Исходный NetGuard'])
with tabs[0]:
    st.subheader('Очистка данных и выделение сигналов')
    st.dataframe(table_ru(pd.DataFrame([cycle['perception']['record']])), use_container_width=True)
    st.bar_chart(pd.Series({ru(k): v for k, v in cycle['perception']['signals'].items()}, name='Сила сигнала'))
    st.caption('41 признак. Поля label и difficulty исключены из расчёта.')
    with st.expander('Журнал очистки и исходная запись'):
        st.json({'Исходные данные': view_ru(raw), 'Очистка': audit_ru(cycle['perception']['audit'])})
    st.download_button('Скачать пример CSV / шаблон загрузки', (ROOT / 'data/demo_flows.csv').read_bytes(),
                       'demo_flows.csv', 'text/csv')
    st.caption('Демонстрационные сценарии синтетические. NSL-KDD содержит реальные записи набора данных, воспроизводимые офлайн. В CSV сохраняйте технические названия столбцов из шаблона.')
with tabs[1]:
    st.subheader('Значимость = сила сигнала × важность правила')
    st.dataframe(table_ru(pd.DataFrame(cycle['attention']['selected'])), use_container_width=True, hide_index=True)
    st.bar_chart(table_ru(pd.DataFrame(cycle['attention']['selected'])).set_index('Сигнал')['Значимость'])
    st.write('Исключённые сигналы:', [ru(r['signal']) for r in cycle['attention']['suppressed']])
    st.caption('В рассуждение поступают только выбранные сигналы. Важности заданы явно; это механизм на правилах, а не нейронное внимание.')
with tabs[2]:
    st.subheader('Сохранённый контекст с подтверждёнными исходами')
    context = cycle['memory']
    st.json(view_ru({k: v for k, v in context.items() if k != 'recent'}))
    st.dataframe(table_ru(pd.DataFrame(context['recent'])), use_container_width=True)
    st.caption('SQLite сохраняет отчёты и обратную связь между запусками. Неподтверждённые прогнозы не становятся метками атак. '
               'Сопоставление по протоколу и сервису может объединять разные хосты.')
with tabs[3]:
    st.subheader('Ход логического вывода')
    for step in reasoning_ru(cycle):
        st.write(step)
    st.caption('Риск — интерпретируемый индекс, а не калиброванная вероятность. Апостериорное распределение Beta оценивает '
               'частоту атак среди случаев данного типа, размеченных аналитиком.')
with tabs[4]:
    st.subheader('Метод взвешенной суммы (WSM)')
    st.latex(r'u_{ij}=x_{ij}/100,\quad u_{ij}=1-x_{ij}/100,\quad S_i=\sum_j\frac{w_j}{\sum_k w_k}u_{ij}')
    st.caption('Первая формула — для выгоды, вторая — для затрат. Фиксированная шкала 0–100 сохраняет абсолютные изменения риска. WSM допускает компенсацию затрат выгодой. '
               'Модель предполагает линейную полезность и не содержит обязательных ограничений безопасности.')
    st.dataframe(table_ru(decision['ranking']), use_container_width=True)
    st.bar_chart(table_ru(decision['contributions']))
    with st.expander('Нормированные значения, веса и вклады'):
        st.write(view_ru(decision['weights']))
        st.dataframe(table_ru(decision['normalized']))
        st.dataframe(table_ru(decision['contributions']))
    st.subheader('Что, если… · те же данные и состояние памяти')
    scenario_weights = {c: st.slider('Что, если: ' + ru(c), 0, 100, int(DEFAULT_WEIGHTS[c]*100), key='whatif_' + c)
                        for c in CRITERIA}
    try:
        scenario = decide(matrix, scenario_weights)
        comparison = decision['ranking'][['Rank', 'Score']].join(
            scenario['ranking'][['Rank', 'Score']], lsuffix=' baseline', rsuffix=' what-if')
        st.dataframe(table_ru(comparison.rename(columns={'Rank baseline': 'Место: исходное', 'Score baseline': 'Оценка: исходная', 'Rank what-if': 'Место: сценарий', 'Score what-if': 'Оценка: сценарий'})), use_container_width=True)
        st.info('Рекомендация сценария: ' + ru(scenario['recommendation']))
        st.write(explanation_ru(scenario))
        st.session_state['whatif_recommendation'] = scenario['recommendation']
    except ValueError as exc:
        st.warning(error_ru(exc))
    sweep = sensitivity(matrix, decision['weights'])
    st.line_chart(table_ru(sweep.pivot(index='Protection weight', columns='Alternative', values='Score')))
    st.caption('График изменяет вес защиты, сохраняя соотношение остальных весов. '
               'Изменение сценария не подтверждает действие автоматически.')
with tabs[5]:
    st.subheader('Решение человека и безопасный отчёт')
    st.write('Выберите любой вариант, в том числе отличающийся от рекомендации. '
             'После подтверждения приложение сохранит JSON-отчёт и запись аудита SQLite на этом компьютере.')
    with st.form('human_decision'):
        chosen = st.selectbox('Итоговый выбор человека', list(matrix.index), format_func=ru, key='human_choice')
        confirmed = st.checkbox('Подтверждаю сохранение локального отчёта о решении', key='confirm_action')
        submitted = st.form_submit_button('Сохранить подтверждённый отчёт', key='save_report')
    if submitted:
        try:
            st.session_state['last_action'] = act(cycle, chosen, confirmed, memory, RUNTIME / 'reports')
        except (ValueError, OSError) as exc:
            st.error(error_ru(exc))
    if 'last_action' in st.session_state:
        report = st.session_state['last_action']
        st.success(f'Отчёт {report["id"][:8]} сохранён. Протокол/сервис: {report["snapshot"]["pattern"]}. Выбор: {ru(report["chosen"])}.')
        st.code(report['path'], language=None)
        st.download_button('Скачать последний подтверждённый отчёт', report['content'], report['id'] + '.json', 'application/json')
        st.json(view_ru({'mode': report['mode'], 'effect': report['snapshot']['effect']}))
        st.caption('Файл JSON сохраняет технические ключи и коды для совместимости с прежней памятью.')
    else:
        st.info('Действие ещё не выполнено. Подтверждение человека завершит шестую стадию.')
with tabs[6]:
    st.subheader('Обучение по подтверждённому исходу')
    st.write('Обратная связь обновляет распределение Beta для протокола/сервиса сохранённого отчёта. '
             'Следующий расчёт использует обученное состояние. Для каждого отчёта допускается только одна метка.')
    if 'last_action' in st.session_state:
        report = st.session_state['last_action']
        st.caption(f'Обратная связь к отчёту {report["id"][:8]}, протокол/сервис: {report["snapshot"]["pattern"]}.')
        label = st.radio('Подтверждённый исход', ['Benign / false alarm', 'Confirmed attack'], format_func=ru, key='feedback_label')
        if st.button('Применить подтверждённую обратную связь', key='apply_feedback'):
            try:
                st.session_state['learning_result'] = learn(memory, report['id'], int(label == 'Confirmed attack'))
                st.rerun()
            except ValueError as exc:
                st.warning(error_ru(exc))
    else:
        st.info('Сначала сохраните подтверждённый отчёт во вкладке «Действие», затем укажите его фактический исход здесь.')
    if 'learning_result' in st.session_state:
        result = st.session_state['learning_result']
        st.dataframe(table_ru(pd.DataFrame({'Состояние': ['При подтверждении решения', 'После обратной связи'],
            'Risk': [result['before_risk'], result['after_risk']],
            'Recommendation': [result['before_choice'], result['after_choice']]})), hide_index=True)
        st.json(view_ru(result))
    if st.button('Запустить отдельную демонстрацию обучения', key='demo_learning'):
        from scripts.demo_learning import demonstrate
        st.session_state['learning_demo'] = demonstrate()
    if 'learning_demo' in st.session_state:
        demo = table_ru(pd.DataFrame(st.session_state['learning_demo']))
        st.dataframe(demo, hide_index=True)
        st.line_chart(demo.set_index('Подтверждённые ложные тревоги')['Риск'])
        st.caption('Во временной базе заданы четыре подтверждённых безопасных исхода. '
                   'Опыт показывает адаптацию на одной записи; он не доказывает рост точности обнаружения и не меняет вашу память.')
with tabs[7]:
    st.subheader('Сохранённые исследования и исходное демо NetGuard')
    st.write('Исходные ноутбуки, данные, рисунки, HTML/JavaScript-интерфейс и маршруты FastAPI сохранены. '
             'Новая когнитивная СППР использует явные правила и обучение по подтверждённым исходам. '
             'Исходное демо отдельно выполняет прогноз случайным лесом на записях NSL-KDD.')
    st.code('python -m uvicorn demo.server:app --host 127.0.0.1 --port 8000')
    st.link_button('Открыть исходное демо (сначала запустите его сервер)', 'http://127.0.0.1:8000')
    metrics = ROOT / 'results/models/rebuilt/metrics.json'
    if metrics.exists():
        st.json(view_ru(json.loads(metrics.read_text(encoding='utf-8'))))
    st.caption('Исходные файлы .pkl содержали указатели Git LFS. Рабочая модель заново обучена на локальном NSL-KDD. '
               'Это отдельный запуск обучения. Обозначения «применения мер» в исходном демо являются имитацией.')

st.divider()
st.caption('Реализовано: обработка данных · внимание · память SQLite · вывод на правилах · СППР WSM · подтверждённый отчёт · обучение по обратной связи. '
           'Реальное управление сетью, захват пакетов и внешние уведомления не реализованы. Практическая эффективность не доказана.')
