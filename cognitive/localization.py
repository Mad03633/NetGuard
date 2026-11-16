"""Russian presentation layer. Stable model, CSV and database identifiers stay unchanged."""
import re
import pandas as pd

LABELS = {
    'Protection': 'Защита', 'Disruption': 'Нарушение работы', 'Effort': 'Трудозатраты',
    'benefit': 'выгода', 'cost': 'затраты', 'Monitor': 'Наблюдение',
    'Analyst review': 'Проверка аналитиком', 'Quarantine proposal': 'Предложение карантина',
    'LOW': 'НИЗКИЙ', 'MEDIUM': 'СРЕДНИЙ', 'HIGH': 'ВЫСОКИЙ',
    'Demo scenarios': 'Демонстрационные сценарии', 'Upload table': 'Загрузка таблицы',
    'NSL-KDD test sample': 'Тестовая выборка NSL-KDD',
    'normal_ftp': 'Обычное FTP-соединение', 'ambiguous_http': 'Неоднозначный HTTP',
    'syn_flood': 'SYN-флуд', 'service_scan': 'Сканирование сервисов', 'failed_login': 'Неудачные входы',
    'connection_flag': 'Флаг соединения', 'syn_errors': 'Ошибки SYN',
    'connection_volume': 'Число соединений', 'service_diversity': 'Разнообразие сервисов',
    'failed_logins': 'Неудачные входы', 'signal': 'Сигнал', 'value': 'Значение',
    'importance': 'Важность', 'salience': 'Значимость', 'Score': 'Оценка', 'Rank': 'Место',
    'Alternative': 'Вариант', 'Protection weight': 'Вес защиты',
    'Verified benign outcomes': 'Подтверждённые ложные тревоги', 'Risk': 'Риск',
    'Recommendation': 'Рекомендация', 'Benign / false alarm': 'Безопасный трафик / ложная тревога',
    'Confirmed attack': 'Подтверждённая атака', 'normal': 'Норма',
    'pattern': 'Протокол и сервис', 'confirmed': 'Подтверждённых исходов',
    'attacks': 'Атаки', 'benign': 'Безопасные соединения', 'alpha': 'Альфа', 'beta': 'Бета',
    'posterior': 'Среднее апостериорного распределения', 'recent': 'Последние отчёты',
    'total_reports': 'Всего отчётов', 'id': 'Номер отчёта', 'report_id': 'Номер отчёта',
    'created': 'Время сохранения (UTC)', 'chosen': 'Выбор человека', 'label': 'Метка',
    'before_risk': 'Риск до обучения', 'after_risk': 'Риск после обучения',
    'before_choice': 'Рекомендация до обучения', 'after_choice': 'Рекомендация после обучения',
    'method': 'Метод', 'comparison': 'Условия сравнения', 'mode': 'Режим', 'effect': 'Результат',
    'LOCAL_REPORT_ONLY': 'ТОЛЬКО ЛОКАЛЬНЫЙ ОТЧЁТ',
    'Beta(1,1) prior + verified attack/benign counts; bounded evidence blend':
        'Априорное Beta(1,1) и подтверждённые метки атак/безопасного трафика; влияние обратной связи ограничено',
    'Stored action vs current learned state; fixed weights and other criteria. Custom Protection scaled with risk.':
        'Сохранённое решение сравнивается с текущим состоянием после обучения. Веса и остальные критерии фиксированы; защита масштабируется с риском.',
    'Saved report only. No firewall changes, notifications or external calls.':
        'Сохранён локальный отчёт. Настройки сети не менялись; уведомления и внешние вызовы не выполнялись.',
    'origin': 'Происхождение', 'model': 'Модель', 'training_rows': 'Обучающих записей',
    'test_rows': 'Тестовых записей', 'data': 'Данные', 'accuracy': 'Доля верных ответов',
    'precision': 'Точность обнаружения атак', 'recall': 'Полнота обнаружения атак',
    'f1': 'F1-мера', 'roc_auc': 'Площадь под ROC-кривой', 'limitation': 'Ограничение',
    'Rebuilt locally because original artifacts are Git LFS pointers':
        'Модель обучена локально, поскольку исходные файлы содержат только указатели Git LFS',
    'RandomForestClassifier (80 trees, depth 22, seed 42)':
        'Случайный лес: 80 деревьев, глубина 22, начальное значение генератора 42',
    'NSL-KDD train/test split; preprocessing fit on training only':
        'Обучающая и тестовая части NSL-KDD; предобработка обучена только на обучающей части',
    'Historical offline data. These are legacy RF metrics, not DSS effectiveness.':
        'Исторические данные. Метрики относятся к исходному случайному лесу и не оценивают эффективность СППР.',
    'protocol_type': 'Протокол', 'service': 'Сервис', 'flag': 'Флаг', 'duration': 'Длительность',
    'src_bytes': 'Байты источника', 'dst_bytes': 'Байты получателя', 'land': 'Совпадение адресов',
    'wrong_fragment': 'Ошибочные фрагменты', 'urgent': 'Срочные пакеты', 'hot': 'Значимые операции',
    'num_failed_logins': 'Неудачные попытки входа', 'logged_in': 'Вход выполнен',
    'num_compromised': 'Компрометации', 'root_shell': 'Оболочка root', 'su_attempted': 'Попытка su',
    'num_root': 'Операции root', 'num_file_creations': 'Созданные файлы', 'num_shells': 'Оболочки',
    'num_access_files': 'Обращения к файлам', 'num_outbound_cmds': 'Исходящие команды',
    'is_host_login': 'Вход хоста', 'is_guest_login': 'Гостевой вход', 'count': 'Соединения с хостом',
    'srv_count': 'Соединения с сервисом', 'serror_rate': 'Доля SYN-ошибок',
    'srv_serror_rate': 'Доля SYN-ошибок сервиса', 'rerror_rate': 'Доля REJ-ошибок',
    'srv_rerror_rate': 'Доля REJ-ошибок сервиса', 'same_srv_rate': 'Доля того же сервиса',
    'diff_srv_rate': 'Доля других сервисов', 'srv_diff_host_rate': 'Доля других хостов сервиса',
    'dst_host_count': 'Соединения с получателем', 'dst_host_srv_count': 'Соединения с сервисом получателя',
    'dst_host_same_srv_rate': 'Тот же сервис получателя', 'dst_host_diff_srv_rate': 'Другие сервисы получателя',
    'dst_host_same_src_port_rate': 'Тот же порт источника', 'dst_host_srv_diff_host_rate': 'Другие хосты сервиса получателя',
    'dst_host_serror_rate': 'SYN-ошибки получателя', 'dst_host_srv_serror_rate': 'SYN-ошибки сервиса получателя',
    'dst_host_rerror_rate': 'REJ-ошибки получателя', 'dst_host_srv_rerror_rate': 'REJ-ошибки сервиса получателя',
}

ERRORS = {
    'File exceeds 5 MB. Upload a smaller sample.': 'Файл превышает 5 МБ. Загрузите меньшую выборку.',
    'Expected a nonempty UTF-8 comma-separated table.': 'Нужна непустая таблица UTF-8 с разделителями-запятыми.',
    'NSL-KDD input requires exactly 43 columns.': 'Для NSL-KDD требуется ровно 43 столбца.',
    'Provide between 1 and 10,000 records.': 'Таблица должна содержать от 1 до 10 000 записей.',
    'top_k must be between 1 and 5.': 'Число выбранных сигналов должно быть от 1 до 5.',
    'Keep the three distinct supported alternatives.': 'Сохраните три предусмотренных варианта без повторов.',
    'Provide all three criteria and weights.': 'Укажите все три критерия и их веса.',
    'Matrix and weights must be numeric.': 'Значения матрицы и весов должны быть числами.',
    'Criterion values must be finite and between 0 and 100.': 'Значения критериев должны быть конечными числами от 0 до 100.',
    'Weights must be finite, nonnegative and have a positive sum.': 'Веса должны быть конечными неотрицательными числами. Их сумма должна быть больше нуля.',
    'Human confirmation is required before writing a report.': 'Перед сохранением отчёта подтвердите решение.',
    'Unsupported action.': 'Этот вариант действия не поддерживается.', 'Unknown action report.': 'Отчёт о решении не найден.',
    'Outcome must be 0 (benign) or 1 (attack).': 'Метка исхода должна быть 0 (безопасно) или 1 (атака).',
    'This report already has feedback; duplicate learning was blocked.': 'Для этого отчёта обратная связь уже сохранена. Повторное обучение заблокировано.',
}


def ru(value):
    return LABELS.get(value, value) if isinstance(value, str) else value


def table_ru(frame):
    """Copy and translate labels/values without modifying the model's DataFrame."""
    result = frame.copy()
    for column in result.columns:
        if result[column].dtype == object:
            result[column] = result[column].map(ru)
    result = result.rename(columns=LABELS, index=LABELS)
    result.index.name = ru(result.index.name)
    result.columns.name = ru(result.columns.name)
    return result


def view_ru(value):
    if isinstance(value, dict):
        return {ru(k): view_ru(v) for k, v in value.items()}
    if isinstance(value, list):
        return [view_ru(v) for v in value]
    return ru(value)


def error_ru(error):
    text = str(error)
    if text in ERRORS:
        return ERRORS[text]
    if text.startswith('Missing required columns: '):
        return 'Отсутствуют обязательные столбцы: ' + text.split(': ', 1)[1]
    patterns = [(r'(.+) cannot be empty\.', 'Поле «{}» не должно быть пустым.'),
                (r'(.+) must be at most 64 characters\.', 'Поле «{}» должно содержать не более 64 символов.'),
                (r'(.+) must be numeric\.', 'Поле «{}» должно содержать число.'),
                (r'(.+) must be finite\.', 'Поле «{}» должно содержать конечное число.')]
    for pattern, translation in patterns:
        match = re.fullmatch(pattern, text)
        if match:
            return translation.format(ru(match[1]))
    return 'Не удалось обработать данные. Подробности: ' + text


def audit_ru(entries):
    result = []
    for entry in entries:
        field, detail = entry.split(': ', 1)
        detail = detail.replace('absent, default 0 (reduced schema)', 'поле отсутствует, принято 0 (сокращённый набор полей)')
        detail = detail.replace('clipped to', 'ограничено до')
        result.append(f'{ru(field)} ({field}): {detail}')
    return result


def explanation_ru(decision):
    winner, runner = decision['ranking'].index[:2]
    delta = decision['contributions'].loc[winner] - decision['contributions'].loc[runner]
    driver = delta.idxmax()
    margin = decision['ranking'].loc[winner, 'Score'] - decision['ranking'].loc[runner, 'Score']
    return (f'«{ru(winner)}» опережает вариант «{ru(runner)}» на {margin:.4f}. '
            f'Наибольшее преимущество даёт критерий «{ru(driver)}» ({delta[driver]:+.4f}). '
            'При равных оценках используется фиксированный порядок вариантов. Итоговый выбор делает аналитик.')


def reasoning_ru(cycle):
    context, reasoning = cycle['memory'], cycle['reasoning']
    return [f'П1. Риск по выбранным сигналам = 0,08 + 0,87 × сумма взвешенных вкладов = {reasoning["base_risk"]:.4f}.',
            f'П2. Подтверждено атак: {context["attacks"]}; безопасных исходов: {context["benign"]}. '
            f'Среднее Beta({context["alpha"]}, {context["beta"]}) = {context["posterior"]:.4f}.',
            f'П3. Влияние обратной связи = min(0,65; n/(n+2)) = {reasoning["learned_strength"]:.4f}. '
            f'Итоговый риск = {reasoning["risk"]:.4f}.',
            f'П4. Низкий риск: < 0,35; средний: < 0,70; иначе высокий. Результат: {ru(reasoning["level"])}.']
