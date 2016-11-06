from sails.ui.sun import SunVoxMainWindow

from .opener import Opener


@Opener.register_opener
class SunVoxOpener(Opener):

    file_ext = '.sunvox'
    file_type_label = 'SunVox'
    main_window_class = SunVoxMainWindow
