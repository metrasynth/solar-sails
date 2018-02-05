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

- MIDI "note on" events.

- Transport control events.

- Output and/or error details while the parameters_ are being defined.

- Output and/or error details while the `project builder`_ is running.

- "Finished loading" messages when the project_ is ready and controllers_ have appeared.

- "Exported synth" messages when a ``.sunsynth`` version of the project_ is saved.

- "Exported project" messages when a ``.sunvox`` version of the project_ is saved.

Workflow detail
===============

Opening an existing MMCK script
-------------------------------

Select the *File > Open* menu, then open a file ending with ``.mmckpy``.
After a script successfully loads, the MMCK main window will appear.

The initial parameters_ will be set if this is the first time you've opened the file.
The previous parameters_ you used will be loaded if you've opened this file already.

MacOS keyboard shortcut: Command+O.

Linux and Windows keyboard shortcut: Ctrl+O.

..  note::

    You can find an assortment of scripts at the `Metrasynth Gallery GitHub repo`_.

..  _Metrasynth Gallery GitHub repo:
    https://github.com/metrasynth/gallery/

Changing parameters
-------------------

In the parameters_ window, change the values to alter how the project_ is built.

After a small delay, your changes will be processed by the `project builder`_.

The controllers_ available for the project_ will appear.

..  note::

    While many parameters have sensible boundaries, keep in mind that some parameter combinations can be potent!
    With some scripts, certain parameter combinations can result in unwanted behavior.

    Some examples of unwanted behavior:
    volumes becoming too loud,
    harsh noises made by a `project builder`_ that utilizes randomness,
    or overloading the SunVox sound engine.

    Just keep your master volume control nearby, and be familiar with your operating system's "force quit" features.


Auditioning notes
-----------------

Use an available MIDI controller to send MIDI note on/off events to Solar Sails.

Notes will be sent to module ``01`` as created by the `project builder`_.

What you hear comes directly from the SunVox audio engine and will sound exactly the same in SunVox itself.

When a note is played, the note and velocity are added to the log_.
Note off events do not appear in the log_.

Auditioning patterns
--------------------

Some scripts are designed to create patterns.

Use the *Transport > Play from beginning* and *Transport > Stop* menu items to control playback.

Play From Beginning keyboard shortcut: F11.

Stop keyboard shortcut: F12.

Adjusting controllers
---------------------

Controllers are presented in "logical" groupings.
This means a single group in MMCK could actually represent several modules.

Use the data entry widget provided to change a controller's value.
If the value is numeric, use the slider or numerical entry widget to set the value.
If the value is discrete, select the desired from the dropdown box.

Or, use a MIDI controller to send CC values to Solar Sails.
The CC values received will be mapped linearly to the value range of the mapped controller_(s).

Use the second combobox to see which CC is mapped to a controller_, or to map it to a different CC.
You can assign a single CC to multiple controllers.
You can also disable a mapping by choosing the first entry, which is blank.

Selecting user defined controllers
----------------------------------

To expose a controller in SunVox, it must be mapped to a `user defined controller`_.
These correspond to controllers 6 to 32 (06h to 20h) in an exported MetaModule.

Use the first combobox to map a controller_ to a `user defined controller`_ slot.

You can map up to 16 controllers to a single slot.
When doing so, a MultiCtl module will be automatically created to propagate value changes accordingly.

Exporting to SunVox clipboard
-----------------------------

When you like a sound, use the *Edit > Copy to SunVox clipboard* menu item.
Then, switch to SunVox, and use the *Paste* action in the module view.
Your module is now ready for immediate use.

MacOS keyboard shortcut: Command+Shift+C.

Linux and Windows keyboard shortcut: Ctrl+Shift+C.

..  note::

    Make sure you have added a workspace path as described in :doc:`getting-started`.

Exporting to a .sunsynth module file
------------------------------------

Use *File > Export MetaModule* menu item.
A time-stamped ``.sunsynth`` filename will be created, and the project_ will be saved to that file as a MetaModule.
The log_ will show the full path of the exported file.

MacOS keyboard shortcut: Command+E.

Linux and Windows keyboard shortcut: Ctrl+E.

Exporting to a .sunvox project file
-----------------------------------

Use *File > Export Project* menu item.
A time-stamped ``.sunvox`` filename will be created, and the project_ will be saved to that file.
The log_ will show the full path of the exported file.

Project files do not contain `user defined controllers`_.

MacOS keyboard shortcut: Command+Shift+E.

Linux and Windows keyboard shortcut: Ctrl+Shift+E.

Restoring parameters from a .sunsynth file
------------------------------------------

(to be written)

Creating your own MMCK scripts
==============================

Creating a .mmckpy file
-----------------------

(to be written)

Specifying parameters
---------------------

(to be written)

Building the MetaModule project
-------------------------------

(to be written)

Auto-reloading
--------------

(to be written)

..  note::

    Some kinds of errors cause the auto-reload to stop working.
    If this happens, quit the Solar Sails app and reopen it.
