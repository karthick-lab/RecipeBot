# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_bot.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pandas._libs.tslibs.timestamps', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.parsing', 'yfinance', 'ta', 'matplotlib', 'matplotlib.backends.backend_tkagg', 'llama_cpp', 'llama_cpp.llama', 'llama_cpp._lib', 'llama_cpp._utils'],
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
    name='RecipeBot',
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
