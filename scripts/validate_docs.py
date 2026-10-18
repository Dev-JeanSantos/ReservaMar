#!/usr/bin/env python3
"""Validação leve dos insumos Kiro; não substitui revisão humana."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
errors = []
steering = list((ROOT / '.kiro/steering').glob('*.md'))
if len(steering) < 5:
    errors.append('Faltam arquivos de steering')
for p in steering:
    body = p.read_text(encoding='utf-8')
    if not body.startswith('---\n') or '\n---\n' not in body[4:]:
        errors.append(f'Front matter ausente: {p.relative_to(ROOT)}')
    if 'inclusion:' not in body.split('---', 2)[1]:
        errors.append(f'Inclusão steering não declarada: {p.relative_to(ROOT)}')
for p in ROOT.rglob('*.md'):
    txt = p.read_text(encoding='utf-8')
    if not txt.strip():
        errors.append(f'Arquivo vazio: {p.relative_to(ROOT)}')
    for m in re.finditer(r'\]\((docs/[^)#]+|\.kiro/[^)#]+)\)', txt):
        target = ROOT / m.group(1)
        if not target.exists():
            errors.append(f'Referência quebrada em {p.relative_to(ROOT)}: {m.group(1)}')
required = ['.kiro/specs/01-foundation-bootstrap/requirements.md',
            'docs/adr/ADR-0001-modular-monolith-and-stack.md',
            'docs/quality/definition-of-done.md',
            'docs/START-IN-KIRO.md']
for path in required:
    if not (ROOT/path).exists():
        errors.append(f'Arquivo requerido ausente: {path}')
for i in range(1,24):
    if f'BR-{i:03d}' not in (ROOT/'.kiro/steering/business-rules.md').read_text():
        errors.append(f'Regra ausente BR-{i:03d}')
print(f'Steering: {len(steering)} | Markdown: {len(list(ROOT.rglob("*.md")))}')
if errors:
    print('Falhas:')
    print('\n'.join(f'- {e}' for e in errors))
    sys.exit(1)
print('OK: estrutura, regras e arquivos fundamentais presentes.')
