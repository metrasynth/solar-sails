# -*- mode: python -*-

import os
import platform
import sys
sys.setrecursionlimit(5000)

import sails.scripts.gui
import sunvox

SAILS_BASE_PATH = os.path.abspath(os.path.dirname(sails.__file__))
SUNVOX_LIB_PATH = os.path.join(os.path.dirname(sunvox.__file__), 'lib')

BITS = 64 if platform.architecture()[0] == '64bit' else 32


def icon(ext):
    return os.path.join(SAILS_BASE_PATH, '..', 'specs', 'solar_sails.{}'.format(ext))


block_cipher = None

datas = []
for ui_dir in [
    '',
    '/mmck',
    '/mmck/controllers',
    '/polyphonist',
    '/settings',
    '/sun/synth',
    '/sun/vox',
]:
    datas.append((
        '../sails/ui{}/*.ui'.format(ui_dir),
        './sails/ui{}'.format(ui_dir),
    ))

binaries = []
if sys.platform == 'win32' and BITS == 32:
    binaries += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'windows', 'lib_x86', 'sunvox.dll'),
            '.',
        ),
    ]
elif sys.platform == 'win32' and BITS == 64:
    binaries += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'windows', 'lib_x86_64', 'sunvox.dll'),
            '.',
        ),
    ]
elif sys.platform == 'linux':
    binaries += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'linux'),
            './sunvox/lib/linux',
        ),
    ]
elif sys.platform == 'darwin':
    binaries += [
        (
            os.path.join(SUNVOX_LIB_PATH, 'osx'),
            './sunvox/lib/osx',
        ),
    ]

a = Analysis(
    [sails.scripts.gui.__file__],
    pathex=[SAILS_BASE_PATH],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'mido.backends.rtmidi',
        'py',
        'py._builtin',
        'py._code.source',
        'py._error',
        'py._path.local',
        'py._std',
        'scipy.special._ufuncs_cxx',
        'scipy.linalg.cython_blas',
        'scipy.linalg.cython_lapack',
        'scipy.integrate',
        'scipy.integrate.quadrature',
        'scipy.integrate.odepack',
        'scipy.integrate._odepack',
        'scipy.integrate.quadpack',
        'scipy.integrate._quadpack',
        'scipy.integrate._ode',
        'scipy.integrate.vode',
        'scipy.integrate._dop',
        'scipy.integrate.lsoda',
        'scipy._lib.messagestream',
        'wave',
        'wavio',
    ],
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
    name='solar-sails',
    icon=icon('ico'),
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
    name='solar-sails',
)

app = BUNDLE(
    coll,
    name='Solar Sails.app',
    icon=icon('icns'),
    bundle_identifier=None,
    info_plist={
        'NSHighResolutionCapable': 'True',
    },
)
