===============
Getting Started
===============

First time configuration
========================

Open the preferences for the app.

On MacOS, open the Solar Sails menu, then click Preferences.

On Linux and Windows, open the File menu, then click Settings.

SunVox tab
----------

The first workspace path listed in this tab will be used for reading/writing SunVox clipboard files.

Click the ``[+]`` button at the bottom.

Navigate to, then choose, the folder containing your SunVox app.

SunVox and Solar Sails both use this location to store SunVox clipboard data.

Audio tab
---------

This tab is not yet functional.

For audio playback, Solar Sails will use the default system output device at the time of application launch.

MIDI tab
--------

Solar Sails will listen to MIDI note and CC events.

MIDI listening is omnichannel.

Solar Sails always listens to the interface named ``Metrasynth Solar Sails``.
On Linux and MacOS, Solar Sails will create this as a virtual interface.
On Windows, use the free loopMIDI_ app to create a virtual interface with this name.

..  _loopMIDI:
    http://www.tobias-erichsen.de/software/loopmidi.html

Interfaces
..........

Available MIDI interfaces are listed here.

Solar Sails listens to selected interfaces.

Click on an interface to select or deselect it.

If you connect an interface while Solar Sails is running, click Refresh.
If an interface was selected in the past, it will be automatically reselected.

Ignore MIDI in background
.........................

Turn this on if you want Solar Sails to ignore MIDI events when in the background.

This can be useful when you are using the same MIDI controller to input notes into SunVox.

CC Mappings
...........

This is a list of CCs that will be auto-assigned to controllers in the :doc:`mmck`.

The format is ``###=Label``.
``###`` is the decimal notation of the CC to listen to.
``Label`` is how you want the CC to be labeled in the user interface.


MetaModule Construction Kit (MMCK)
==================================

MMCK is a powerful tool for creating new SunVox MetaModules.

Find out more at :doc:`mmck`.


Polyphonist
===========

This tool is currently broken.

These docs will be updated once it's fixed.
