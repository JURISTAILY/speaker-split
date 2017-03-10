import os.path

from core import Track
from settings import RECORDINGS_DIR


if __name__ == '__main__':

    track = Track.from_file(os.path.join(RECORDINGS_DIR, 'dialog2.wav'), channel=0)
    result = track.transcript()
    print(result)
