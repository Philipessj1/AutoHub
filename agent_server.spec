# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hidden_imports = []
hidden_imports += collect_submodules('automations')
hidden_imports += collect_submodules('core')
hidden_imports += collect_submodules('utils')

a = Analysis(
    ['agent/agent_server.py'],
    pathex=[os.path.abspath(".")],
    binaries=[],
    datas=[
        ('automations', 'automations'),
        ('utils', 'utils'),
        ('core', 'core'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='autohub_agent',
    icon='icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Autohub Agent',
)