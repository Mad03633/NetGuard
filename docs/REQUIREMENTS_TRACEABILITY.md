# Assignment coverage and evidence

Source: supplied `Final_Cognitive_System_DSS_EN.docx`, read in full before implementation. Maximum 100 points: Technical 40, PDF 40, Streamlit 20. Defense stages 5/2/3 minutes. This table records implemented evidence, not a claimed grade.

| Criterion | Evidence |
|---|---|
| T1 | `perception.py`: CSV/NSL-KDD parsing, clipping audit, signals; Perception tab. |
| T2 | `attention.py`: salience top-k directly changes risk; Attention tab and slider; downstream test. |
| T3 | `memory.py`: SQLite retrieval influences reasoning; restart persistence and pattern isolation tests. |
| T4 | `reasoning.py`: four inference steps combining evidence and learned context; Reasoning tab. |
| T5 | `decision.py`: explicit WSM alternative selection; Decision tab. |
| T6 | `action.py`: confirmed local report and audit write; Action tab; actual file test. |
| T7 | `learning.py`: online Beta posterior from verified report outcomes; duplicate blocking; before/after demonstration. |
| D1 | Three alternatives, three benefit/cost criteria, user sliders and editable matrix. |
| D2 | Anchored WSM with normalized weights; hand-calculation test, invalid value checks; formula and justification in UI/README. |
| D3 | Ranking, score chart and explicit recommended alternative. |
| D4 | Contributions, winner versus runner-up margin and largest advantage. |
| D5 | Independent live what-if sliders plus 21-point sensitivity sweep. |
| E1 | Connected evaluate → human-approved act → verified learn → subsequent retrieval. |
| E2 | `streamlit run streamlit_app.py`, requirements, local data and ZIP. |
| Q | Defense guide describes methods and limitations; actual oral understanding must be demonstrated. |
| P1 | PDF problem, SOC analyst and final human triage decision. |
| P2 | PDF seven-stage architecture with feedback loop and DSS/human layer. |
| P3 | PDF stage methods and outputs, plus timed speaker notes in defense guide. |
| P4 | PDF WSM alternatives/criteria, weights, example scores and human choice. |
| P5 | PDF test evidence, controlled learning result, limitations and ethics. |
| P6 | PDF 10 slides, visual elements, large type, concise labels. |
| P7 | 5-minute script provided; actual delivery remains a live defense requirement. |
| U1 | AppTest checks and real HTTP health check; actual desktop demo still required. |
| U2 | Scenario selection, CSV/TXT upload, row selection and attention/weight controls. |
| U3 | Seven numbered Streamlit tabs expose all seven outputs. |
| U4 | Weights, ranking/contributions, recommendation/explanation, interactive what-if. |
| U5 | Consistent layout, visible headline recommendation, charts and explanatory labels. |
| U6 | Prepared 2-minute demo route in defense guide; actual timing is the student's responsibility. |

## Scope boundaries

New Streamlit DSS: implemented and tested. Local report action: implemented. Online pattern learning: implemented. Real packet capture, firewall/quarantine enforcement, analyst identity verification, production validation and causal evidence of improved security: not implemented. Legacy trained-model reproduction: new RF only, clearly separated from original unavailable LFS artifacts. No claim that all original notebook experiments were rerun.
