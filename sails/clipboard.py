import os

from sails.ui import App


def module_clipboard_path():
    workspace_paths = App.settings.value('sunvox/workspace_paths')
    if len(workspace_paths) == 0:
        raise RuntimeError('To copy to SunVox clipboard, set a workspace path in app settings')
    path = workspace_paths[0]
    filename = os.path.join(path, '.sunvox_clipboard.sunsynth')
    return filename
