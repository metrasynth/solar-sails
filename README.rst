Overview of Solar Sails
=======================

..  start-badges

|githubstatus| |appveyorstatus| |docs|

.. |githubstatus| image:: https://github.com/metrasynth/solar-sails/workflows/Build%20and%20Test/badge.svg
    :alt: Build Status
    :scale: 100%
    :target: https://github.com/metrasynth/solar-sails/actions

.. |appveyorstatus| image:: https://ci.appveyor.com/api/projects/status/r56dscldcaxw56tq?svg=true
    :alt: Windows Build Status
    :scale: 100%
    :target: https://ci.appveyor.com/project/gldnspud/solar-sails

.. |docs| image:: https://readthedocs.org/projects/solar-sails/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://solar-sails.readthedocs.io/en/latest/?badge=latest

..  end-badges

"SunVox Augmentation and Interactive Live-coding System"

Solar Sails is a cross-platform app that augments the SunVox_
modular music studio.

..  _SunVox:
    http://warmplace.ru/soft/sunvox/

It combines `Radiant Voices`_, `Solar Flares`_, and sunvox-dll-python_
into a downloadable app that provides a workspace to make use of those tools.

..  _Radiant Voices:
    https://radiant-voices.readthedocs.io/

..  _Solar Flares:
    https://solar-flares.readthedocs.io/

..  _sunvox-dll-python:
    https://sunvox-dll-python.readthedocs.io/


Downloading and installing
--------------------------

Solar Sails is still alpha-quality software.

Please follow the steps outlined in the `installation`_ docs.

..  _installation:
    https://solar-sails.readthedocs.io/en/latest/installing.html


Requirements for downloadable app
---------------------------------

- MacOS 10.11 El Capitan, or later

- Windows 7, or later, 64-bit install

- Linux, 64-bit install, Ubuntu 16.04 or equivalent


Requirements for building from source
-------------------------------------

- Python 3.12 or later

- OS supported by PyQt6_ and sunvox-dll-python_.

- uv_ package manager

..  _PyQt6:
    https://pypi.org/project/PyQt6/

..  _uv:
    https://github.com/astral-sh/uv


Development setup
-----------------

To set up a development environment:

1. Install uv if not already installed::

    curl -LsSf https://astral.sh/uv/install.sh | sh

2. Clone the repository and navigate to the project directory::

    git clone https://github.com/metrasynth/solar-sails.git
    cd solar-sails

3. Install Python 3.12 and sync dependencies::

    uv python install 3.12
    uv sync --all-extras

4. Install the package in editable mode::

    uv pip install -e .

5. Run the application::

    uv run sails-gui

6. Run tests::

    uv run pytest


Metrasynth
----------

Solar Sails is part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/
