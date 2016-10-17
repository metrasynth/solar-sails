def play(session):
    """
    :type session: s4ils.session.Session
    """
    pos = (-1, 0)
    last_ctl_pos = max(session._ctl_timelines)
    with session[last_ctl_pos]:
        last_cmd_pos = max(session.cmd_timeline)
    while pos <= last_cmd_pos:
        with session[pos] as cpos:
            cmds = session.cmd_timeline.get(pos, [])
            for cmd in cmds:
                print('pos={!r} cmd={!r}'.format(pos, cmd))
            pos = (cpos + 1).pos
