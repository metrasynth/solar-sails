..  code-block:: uml

    @startuml
    rectangle sailsd {
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
    rectangle sails_console
    rectangle sails_midi_clock
    rectangle sails_midi_in
    rectangle sails_midi_out
    rectangle sails_monitor
    rectangle sunvosc

    command_logger ---> commandlog
    command_logger --> sails_monitor

    control_logger ---> controllog
    control_logger --> sails_monitor

    control_timeline -> control_logger

    ipython_engine --> control_timeline

    sails_console <.> ipython_engine : zmq
    sails_midi_in .> control_service : osc

    control_service --> control_timeline

    control_timeline -> command_timeline
    command_timeline --> loop

    clock <-up-> loop

    loop -> sunvox
    loop -> midi
    loop -> generators
    loop --> ticker
    loop ---> command_logger

    ticker ...> sails_midi_clock : osc

    generators -up-> command_timeline

    sunvox <...> sunvosc : osc\n(bidirectional)

    midi ...> sails_midi_out : osc

    @enduml
