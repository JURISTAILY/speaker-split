from core import Dialog
import time


if __name__ == '__main__':

    dialog = Dialog('audio_samples/dialog22.wav')
    t = dialog.track_operator

    print('=' * 80)
    print(t.transcript())

    time.sleep(20)
