==================================
MetaModule Construction Kit (MMCK)
==================================

Solar Sails' MMCK lets you instantly create new SunVox MetaModules using scripts written in the Python_ language.

..  _Python:
    https://www.python.org/

Workflow overview
=================

1.  Open a ``.mmckpy`` file.

2.  Change parameters to your liking.

3.  Audition sounds by sending notes from a MIDI controller.
    Adjust SunVox controllers on-screen, or using CC values sent from a MIDI controller.

4.  Choose the SunVox controllers to assign to up to 27 user defined controllers.

5.  Copy the MetaModule to the SunVox clipboard,
    or save the MetaModule to a ``.sunsynth`` or ``.sunvox`` file.

..  note::

    If you don't have a hardware MIDI controller, try using SunVox itself.
    Create a MultiSynth module and set its MIDI output to ``Metrasynth Solar Sails``.

Concepts
========

MMCK script
-----------

A Python script containing specifications for parameters_ and a `project builder`_.
Their filenames end with the ``.mmckpy`` extension.

Project
-------

The SunVox project contained within the MetaModule.

Parameters
----------

Values that control aspects of how a project_ is created.
The values given by the user are passed directly to the `project builder`_.

Project builder
---------------

The code that builds the actual project, making use of the `Radiant Voices`_ API.
The resulting project is based on the parameters_ given by the user,
processed by algorithms implemented by the `MMCK script`_.

..  _Radiant Voices:
    https://radiant-voices.readthedocs.io/en/latest/

Controllers
-----------

These refer to SunVox module controllers, grouped and presented in a way that is specified by the `MMCK script`_.
As parameters_ are changed, controllers may be added or removed.

You can adjust the value of the controller using standard keyboard and mouse controls.

For each controller, you can specify a `user defined controllers`_ slot to assign it to.

You can also specify a MIDI CC number to use for adjusting the SunVox controller.
CCs are automatically assigned to controllers in the order they are listed in Solar Sails preferences.

See :doc:`getting-started` for how to make CCs available for use.

User defined controllers
------------------------

These are the controllers_ exposed via the user defined controllers of the exported SunVox MetaModule.

Multiple controllers can be grouped into a single "macro" user defined controller.
To do so, assign more than one controller to a single user defined controller slot.

Log
---

Textual feedback from the `MMCK script`_ and the Solar Sails app itself.

The log is cleared whenever a `MMCK script`_ is loaded, or whenever parameters_ are changed.

Here are some types of information you can expect to see in the log:

- Output and/or error details while the parameters_ are being defined.

- Output and/or error details while the `project builder`_ is running.

- "Finished loading" messages when the project_ is ready and controllers_ have appeared.

- "Exported synth" messages when a ``.sunsynth`` version of the project_ is saved.

- "Exported project" messages when a ``.sunvox`` version of the project_ is saved.

Workflow detail
===============

Loading an existing MMCK script
-------------------------------

Auditioning sounds
------------------

Adjusting controllers
---------------------

Selecting user defined controllers
----------------------------------

Creating your own MMCK scripts
==============================

Creating a .mmckpy file
-----------------------

Specifying parameters
---------------------

Building the MetaModule project
-------------------------------

Auto-reloading
--------------

..  note::

    Some kinds of errors cause the auto-reload to stop working.
    If this happens, quit the Solar Sails app and reopen it.
