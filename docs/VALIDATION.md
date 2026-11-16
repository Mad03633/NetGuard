# Recorded validation

## Русская версия

После русификации интерфейса и презентации пройден **31 тест**, без ошибок. Две проверки локализации дополнительно подтверждают русские подписи, сохранение внутренних идентификаторов и передачу отредактированных русских значений матрицы в расчёт WSM. Проверены сценарии, веса, анализ «что, если», действие и обратная связь. Реальный сервер Streamlit на порту 8501 вернул **200 / ok**; русский интерфейс просмотрен в браузере.

PDF переведён на русский вместе с заметками докладчика. Сохранены 10 слайдов, исходные диаграммы, численные результаты и ограничения. Проверены изображения всех 10 страниц после сборки PDF. Русские тексты содержат от 16 до 39 слов на слайд без дублирования технического представления таблиц. Шрифт основного текста сохранён не менее 18 пт в итоговом масштабе.

Форматы CSV/JSON и коды в базе данных сохранены для совместимости. Служебные панели стандартных компонентов Streamlit и отдельное исходное демо не относятся к переводу пользовательского содержимого новой СППР. Сборка ZIP обновлена с русским PDF и `README_RU.md`.

## Первоначальная проверка до перевода

Verified on 16 November 2026 using Windows, Python 3.12.14 and the environment recorded in `requirements-lock.txt`.

- `python -m pytest -q`: **29 passed**, 0 failures. Two deprecation warnings originate from the retained FastAPI/Starlette/httpx test-client dependencies. They do not represent application failures.
- `python -m pip check`: **No broken requirements found**.
- Real Streamlit server: `http://127.0.0.1:8501/_stcore/health` returned **200 / ok**.
- Browser inspection: Streamlit displayed the scenario inputs, seven numbered cognitive tabs, current recommendation, WSM formula, ranking and criterion contribution chart. Desktop layout inspected at 1440×1000; narrow viewport also loaded. The app ran without an exception.
- Real legacy server: `http://127.0.0.1:8000/` returned **200**. Tests exercised existing stream, all four scenario injections, custom analysis and memory APIs using isolated legacy memory.
- Deterministic learning fixture: risk **0.654200, 0.547244, 0.452100, 0.381680, 0.337303**; recommendation changed **Quarantine proposal → Analyst review** after three verified benign outcomes. The isolated demo does not modify runtime memory.
- Rebuilt legacy RF: 125,973 training rows, 22,544 held-out NSL-KDD test rows, train-only preprocessing. Accuracy 0.773820, precision 0.968160, recall 0.623159, F1 0.758261, ROC AUC 0.970884. These measure the RF only. Source: `results/models/rebuilt/metrics.json`.
- PDF: 10 slides, visual diagrams/tables/charts, original body type 24 px or larger on a 1280×720 canvas (18 pt equivalent on a 960×540 pt PDF page). All slides visually inspected; arrow direction and crowded signal labels corrected before final PDF.
- Submission rehearsal: the ZIP was extracted into a separate directory, all 183 packaged file hashes matched its SHA256 manifest, and the extracted copy passed **all 29 tests** using the verified project environment. A separate real Streamlit server started from the extracted directory on port 8502 and returned **200 / ok**, then was stopped. No virtual environment or live runtime memory is included. ZIP integrity (CRC) was also checked.

## Reproducibility boundaries

The new Streamlit application runs independently of the legacy models. Included compatibility RF binaries were newly trained because original .pkl files are Git LFS pointers. Other original notebook experiments and deployment configurations were preserved but not rerun. API regression tests and the restored local RF do not validate all historical research claims.

No production traffic capture, firewall control, actual quarantine or external notification was tested or claimed. Human confirmation produces only a local report. Feedback adaptation is implemented; improved accuracy or real operational benefit is not established. Live demo timing and oral defense remain the student's responsibility.
