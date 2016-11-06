from sails.ui.sun import SunSynthMainWindow

from .opener import Opener


@Opener.register_opener
class SunSynthOpener(Opener):

    file_ext = '.sunsynth'
    file_type_label = 'SunSynth'
    main_window_class = SunSynthMainWindow
