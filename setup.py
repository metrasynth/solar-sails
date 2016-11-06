"""
Solar Sails aims to provide powerful and flexible tools
to augment the SunVox_ modular music studio.

..  _SunVox:
    http://warmplace.ru/soft/sunvox/

Current tools include:

Polyphonist
    Transforms monophonic-only metamodules into polyphonic equivalents.

Visit the `Solar Sails docs`_ for more information.

..  _Solar Sails docs:
    http://solar-sails.rtfd.io/
"""

from setuptools import find_packages, setup

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

setup(
    name='solar-sails',
    version='0.1.0',
    url='https://github.com/metrasynth/solar-sails',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description='Solar Sails: Augmentation and Interactive Live-coding for SunVox',
    long_description=__doc__,
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
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
