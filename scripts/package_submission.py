"""Package the existing project plus new source/data/docs; omit environments and private runtime state."""
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.venv', 'venv310', '.tmp', '.build', '.pytest_cache', '__pycache__', '.git', 'runtime'}


def package():
    output = ROOT / 'submission/NetGuard_Cognitive_DSS.zip'
    files = []
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if not path.is_file() or any(p in EXCLUDED or p.startswith('runtime_') for p in relative.parts):
            continue
        if relative.parts[0] == 'submission' and path.suffix.lower() != '.pdf':
            continue
        if path.suffix.lower() in {'.pyc', '.sqlite3', '.sqlite3-journal'}:
            continue
        files.append(path)
    files.sort()
    checksums = '\n'.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(ROOT).as_posix()
                          for p in files) + '\n'
    with ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            archive.write(path, 'NetGuard-cognitive/' + path.relative_to(ROOT).as_posix())
        archive.writestr('NetGuard-cognitive/SHA256SUMS.txt', checksums)
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        for required in ['streamlit_app.py', 'requirements.txt', 'data/demo_flows.csv',
                         'submission/NetGuard_Cognitive_DSS.pdf', 'cognitive/learning.py']:
            assert 'NetGuard-cognitive/' + required in names
    print(f'{output}\n{len(files)} files + SHA256 manifest; {output.stat().st_size:,} bytes; CRC verified')


if __name__ == '__main__':
    package()
