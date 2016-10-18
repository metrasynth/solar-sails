s4ils
=====

Solar sails for SunVox.

"Synchronized SunVox synth/sequence interactive livecoding system".

|buildstatus| |docs|

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Purpose
-------

Livecoding SunVox w/ support for multiuser and MIDI.


Requirements
------------

- Python 3.5


Quick start
-----------

s4ils is not yet published to PyPI,
so please install using git for the time being.
Here's an example using Linux/macOS::

    $ git clone https://github.com/metrasynth/sunvox-dll-python
    $ git clone https://github.com/metrasynth/orbitant
    $ git clone https://github.com/metrasynth/radiant-voices
    $ git clone https://github.com/metrasynth/s4ils
    $ git clone https://github.com/metrasynth/s4ils
    $ pip install -e sunvox-dll-python
    $ pip install -e orbitant
    $ pip install -e radiant-voices
    $ pip install -e s4ils
    $ pip install -e s4ils


.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/s4ils.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/metrasynth/s4ils

.. |docs| image:: https://readthedocs.org/projects/s4ils/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://s4ils.readthedocs.io/en/latest/?badge=latest
