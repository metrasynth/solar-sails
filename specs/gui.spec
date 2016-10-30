# -*- mode: python -*-

import os
import sys

import s4ils.scripts.gui
import sunvox

S4ILS_BASE_PATH = os.path.abspath(os.path.dirname(s4ils.__file__))
SUNVOX_LIB_PATH = os.path.join(os.path.dirname(sunvox.__file__), 'lib')

block_cipher = None

datas = [
    ('../s4ils/ui', './s4ils/ui'),
]

if sys.platform == 'win32':
    datas += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'windows', 'lib_x86', 'sunvox.dll'),
            '.',
        ),
    ]
elif sys.platform == 'linux':
    datas += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'linux'),
            './sunvox/lib/linux',
        ),
    ]
elif sys.platform == 'darwin':
    datas += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'osx'),
            './sunvox/lib/osx',
        ),
    ]

a = Analysis(
    [s4ils.scripts.gui.__file__],
    pathex=[S4ILS_BASE_PATH],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='s4ils-gui',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='s4ils-gui',
)

app = BUNDLE(
    coll,
    name='S4ils.app',
    icon=None,
    bundle_identifier=None,
)
