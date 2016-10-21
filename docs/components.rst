..  code-block:: uml

    @startuml
    rectangle s4ilsd {
        rectangle control {
            rectangle ipython_engine as "ipython\nengine"
            rectangle control_service as "control\nservice"
        }
        rectangle session {
            rectangle control_timeline as "control\ntimeline"
            rectangle command_timeline as "command\ntimeline"
        }
        rectangle playback {
            rectangle clock
            rectangle engines {
                rectangle sunvox
                rectangle midi
            }
            rectangle loop
            rectangle generators
            rectangle ticker
        }
        rectangle event_logger {
            rectangle command_logger as "command\nlogger"
            rectangle control_logger as "control\nlogger"
        }
    }
    storage commandlog as "command\nlog"
    storage controllog as "control\nlog"
    rectangle s4ils_console
    rectangle s4ils_monitor
    rectangle s4ils_midi_clock
    rectangle s4ils_midi_in
    rectangle s4ils_sunvox_out
    rectangle s4ils_midi_out

    command_logger ---> commandlog
    control_logger ---> controllog

    command_logger --> s4ils_monitor
    control_logger --> s4ils_monitor

    loop ---> command_logger
    control_timeline -> control_logger

    ipython_engine --> control_timeline
    s4ils_console <-> ipython_engine

    s4ils_midi_in --> control_service

    control_service --> control_timeline

    control_timeline -> command_timeline
    command_timeline --> loop
    clock <-up-> loop

    loop --> ticker

    ticker ---> s4ils_midi_clock

    loop -> sunvox
    loop -> midi

    loop -> generators
    generators -up-> command_timeline

    sunvox ---> s4ils_sunvox_out
    midi ---> s4ils_midi_out

    @enduml
