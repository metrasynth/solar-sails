""""""

from setuptools import find_packages, setup

dependencies = [
    'ipykernel',
    'ipython',
    'prompt-toolkit',
    'pyqt5',
    'pyrsistent',
    'quamash',
    'solar-flares',
]

setup(
    name='s4ils',
    version='0.1.0',
    url='https://github.com/metrasynth/s4ils',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description='Multitrack live-coding environment for SunVox',
    long_description=__doc__,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            's4ilsd=s4ils.scripts.s4ilsd:main',
            's4ils-console=s4ils.scripts.console:main',
            's4ils-gui=s4ils.scripts.gui:main',
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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
