"""SunVox Augmentation and Interactive Live-coding System"""

import io
import os
import re
import sys
from setuptools import find_packages, setup

SETUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(SETUP_DIR)
import sails  # NOQA isort:skip

dependencies = [
    'ipykernel',
    'ipython',
    'prompt-toolkit',
    'pyqt5',
    'pyrsistent',
    'python-osc',
    'quamash',
    'solar-flares',
    'sunvosc',
]


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='solar-sails',
    version=sails.__version__,
    url='https://github.com/metrasynth/solar-sails',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description=__doc__,
    long_description='%s\n%s' % (
        re.compile(r'^\.\.\s+start-badges.*^\.\.\s+end-badges', re.M | re.S).
            sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'sailsd=sails.scripts.sailsd:main.start',
            'sails-console=sails.scripts.console:main.start',
            'sails-gui=sails.scripts.gui:main.start',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
