"""Offline checks for the design-stage repository. No dependencies or network."""
from pathlib import Path

REQUIRED = {
    'README.md': ('Not a power meter', 'No live collection'),
    'docs/DESIGN.md': (
        'not a meter reading', 'GET-only', 'No paid services',
        'Unknown model profiles', 'missing samples', 'synthetic',
        'encrypted', 'OAuth', 'disabled',
    ),
}


def validate(root: Path) -> list[str]:
    errors = []
    for filename, phrases in REQUIRED.items():
        path = root / filename
        if not path.is_file():
            errors.append(f'missing file: {filename}')
            continue
        text = path.read_text(encoding='utf-8')
        for phrase in phrases:
            if phrase.casefold() not in text.casefold():
                errors.append(f'{filename}: missing required design guardrail')
        if '\x00' in text:
            errors.append(f'{filename}: contains NUL')
    return errors


if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print('Documentation validation passed.')
