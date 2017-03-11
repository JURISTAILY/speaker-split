import os.path

from core import Track, Dialog
from settings import RECORDINGS_DIR


if __name__ == '__main__':

    dialog = Dialog.from_file(os.path.join(RECORDINGS_DIR, 'dialog2.wav'))
    result = dialog.transcript()
    print(result)
