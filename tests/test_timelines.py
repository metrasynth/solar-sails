from sails.api import INIT, Session, c, n


def test_note_on_off():
    s = Session()

    with s[INIT]:
        s.engine = c.Engine() | s
        s.track = s.engine.track(0)

    with s[0, 0]:
        s.note = c.NoteOn(n.C5, module=0) | s.track | s

    with s[4, 0]:
        s.note.off() | s

    with s[-1, 0]:
        cmds = s.cmd_timeline
        assert INIT not in cmds
        assert (0, 0) not in cmds
        assert (4, 0) not in cmds

    with s[INIT]:
        cmds = s.cmd_timeline
        assert len(cmds[INIT]) == 1
        assert (0, 0) not in cmds
        assert (4, 0) not in cmds

    with s[0, 0]:
        cmds = s.cmd_timeline
        assert len(cmds[INIT]) == 1
        assert len(cmds[0, 0]) == 1
        assert (4, 0) not in cmds

    with s[4, 0]:
        cmds = s.cmd_timeline
        assert len(cmds[INIT]) == 1
        assert len(cmds[0, 0]) == 1
        assert len(cmds[4, 0]) == 1
