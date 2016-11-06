Overall design of Solar Sails
=======================

Solar Sails is a live production tool, specifically designed to leverage
the features of SunVox via its DLL.

The three pillars of the Solar Sails design:

- a set of control events generate changes to a set of command events
- a set of command events alter the state of playback engines
- timing of events are precisely synchronized to a shared clock

In a Solar Sails session:

- all events are time coded by (beat, tick), relative to start of session playback
- a session is persisted with all external resources bundled into a directory
- a log of performed control events and command events are always persisted
- a set of all control events and command events are always persisted
- raw master audio output is optionally persisted

A Solar Sails session can be exported as a playable SunVox project,
for use such as embedding into another Solar Sails session,
or further mastering using SunVox or other tools.


Timecodes
---------

Each beat represents a typical quarter note.

Each beat has 24 ticks.

A time code is a tuple of (beat, tick).

(0, 0) represents the first tick at start of playback.

(0, 23) represents the last tick of the first quarter note of playback.

(1, 0) represents the second tick.

Negative time codes retain an incrementing tick counter.
For example, (-2, 23) is one tick before (-1, 0).


Command events
--------------

These send commands to the the audio and music engines.

Examples of command events:

- create a new sunvox process and sync it to clock
- load a module into sunvox process
- send a command to play a note, or change a controller value
- send a MIDI command out
- load a note generator and give it some inputs

Control events
--------------

These can make changes to the command timeline, at any time code.

Examples of control events:

- blocks of code
- user inputs received (e.g. controller changes, MIDI notes)
- activation/deactivation of note generators
- activation of transport controls
- undo last command timeline change


The flow of time
================


Initialization events
---------------------

Symbolically, this occurs at (-1, 0) on the timeline.

Command events are executed that initialize the system,
such as to start the clock process.

No audio output is generated at this point.


Preparation events
------------------

Symbolically, these occur at (-1, 1) on the timeline.

Control events can be executed to get a session's basic tools and variables
initialized, such as modules and routing, chord structures and arpeggiators,
setting a random number generator seed, and so forth.


Start of audio playback
-----------------------

Once any preparation event starts audio playback:

1. Remaining preparation events will be processed.
2. Tick will advance to (-1, 23).
3. Playback engines will be started.
4. Clock generator will be started.


Processing ticks
----------------

Whenever a tick is processed:

1.  Control events for that tick are applied.
2.  Command events for that tick are executed.

All events are processed sorted by priority and insertion order.


Audio output manager
====================

Dynamic buffer
--------------

Keep a low latency


Mixer
-----

Mixes output of multiple SunVox audio streams.

Handles output to master and output to cue.


Clock time calculator
---------------------




Clock unit
==========

Clock ticker
------------

MIDI clock generator
--------------------



Performance unit
================

Network view of modules.

Choose from templates

-

- mixing



Notes
=====

- Fix bug where tick might occur twice because it's at a buffer boundary.
