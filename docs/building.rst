====================
Building Solar Sails
====================

macOS
=====

From a Python 3.6 virtualenv ::

    $ pyinstaller -y specs/gui.spec

Windows
=======

Install Anaconda Python 3.6, 64-bit.

conda create -n sv36 python=3.6 anaconda

activate sv36

python -m venv env

env\scripts\activate

for each repo, pip install -e ., in this order:

- sunvox-dll-python
- radiant-voices
- orbitant
- sunvosc
- solar-flares
- solar-sails

pip install pypiwin32 pyinstaller


Linux
=====

Ensure python 3.6 is installed

kxstudio:

  apt-get -y install git curl build-essential

  use pyenv-installer to install pyenv

