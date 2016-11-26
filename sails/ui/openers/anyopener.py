from . import Opener


class AnyOpener(Opener):

    caption = 'Open file'

    def __init__(self, parent):
        super(AnyOpener, self).__init__(parent)

    @classmethod
    def filter(cls):
        return 'Supported Files ({})'.format(
            ' '.join(
                '*{}'.format(file_ext) for file_ext in cls._opener_classes
            )
        )
