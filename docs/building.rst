====================
Building Solar Sails
====================

macOS
=====

From a Python 3.5 virtualenv ::

    $ pyinstaller -y specs/gui.spec

Windows
=======

Install Anaconda Python 3.5

conda create -n sv35 python=3.5 anaconda

activate sv35

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

Ensure python 3.5 is installed

kxstudio:

  apt-get -y install git curl build-essential

  use pyenv-installer to install pyenv

