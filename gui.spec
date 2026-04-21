# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

datas_fitz, binaries_fitz, hiddenimports_fitz = collect_all('fitz')
datas_pymupdf, binaries_pymupdf, hiddenimports_pymupdf = collect_all('pymupdf')

a = Analysis(
    ['gui.py'],
    pathex=[],
    datas=datas_fitz + datas_pymupdf,
    binaries=binaries_fitz + binaries_pymupdf,
    hiddenimports=hiddenimports_fitz + hiddenimports_pymupdf + ['fitz.frontend'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
