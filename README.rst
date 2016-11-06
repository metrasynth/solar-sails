Solar Sails: Augmentation and Interactive Live-coding for SunVox
================================================================

|buildstatus| |docs|

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Purpose
-------

Solar Sails aims to provide powerful and flexible tools
to augment the SunVox_ modular music studio.

..  _SunVox:
    http://warmplace.ru/soft/sunvox/

Current tools include:

Polyphonist
    Transforms monophonic-only metamodules into polyphonic equivalents.

Visit the `Solar Sails docs`_ for more information.

..  _Solar Sails docs:
    https://solar-sails.readthedocs.io/en/latest/


Requirements
------------

- Python 3.5


Quick start
-----------

Solar Sails is not yet published to PyPI,
so please install using git for the time being.
Here's an example using Linux/macOS::

    $ git clone https://github.com/metrasynth/sunvox-dll-python
    $ git clone https://github.com/metrasynth/orbitant
    $ git clone https://github.com/metrasynth/radiant-voices
    $ git clone https://github.com/metrasynth/solar-flares
    $ git clone https://github.com/metrasynth/solar-sails
    $ pip install -e sunvox-dll-python
    $ pip install -e orbitant
    $ pip install -e radiant-voices
    $ pip install -e solar-flares
    $ pip install -e solar-sails


.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/solar-sails.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/metrasynth/solar-sails

.. |docs| image:: https://readthedocs.org/projects/solar-sails/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://solar-sails.readthedocs.io/en/latest/?badge=latest
