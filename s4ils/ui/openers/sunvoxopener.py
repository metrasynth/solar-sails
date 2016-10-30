from s4ils.ui.sunvoxmainwindow import SunVoxMainWindow
from s4ils.ui.openers.opener import Opener


@Opener.register_opener
class SunvoxOpener(Opener):

    file_ext = '.sunvox'
    file_type_label = 'SunVox'
    main_window_class = SunVoxMainWindow

    def exec_(self, filename=None):
        if filename is None:
            filename, _ = self.requested_filename()
        if filename:
            return self.new_or_existing_window(filename)
        else:
            return None
