"""Reassemble the visually checked native slide renders into the required PDF.

Optional build dependency: reportlab (the application itself does not need it).
Usage: python -m scripts.build_pdf [directory of slide-01.png ... slide-10.png]
"""
from pathlib import Path
import sys
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]


def build(source=None):
    folder = Path(source) if source else ROOT / 'docs/presentation_source'
    pages = [folder / f'slide-{i:02}.png' for i in range(1, 11)]
    for page in pages:
        if not page.is_file():
            raise FileNotFoundError(page)
    output = ROOT / 'submission/NetGuard_Cognitive_DSS.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(output), pagesize=(960, 540))
    canvas.setTitle('Когнитивная СППР NetGuard')
    canvas.setAuthor('Команда проекта NetGuard')
    canvas.setSubject('Когнитивный цикл, СППР WSM, обучение по обратной связи и ограничения')
    for page in pages:
        canvas.drawImage(str(page), 0, 0, width=960, height=540)
        canvas.showPage()
    canvas.save()
    print(output)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
