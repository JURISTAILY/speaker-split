import os.path

from dialog import Track, Dialog


class Engine:
    def process_new_recording(self, filename):

        tr_1 = Track.from_file(filename, channel=0)
        tr_2 = Track.from_file(filename, channel=1)
        dialog = Dialog(track_client=tr_1, track_operator=tr_2)

        info = dialog.get_silence_info()
        info.update(dialog.get_interruptions_info())

        return {
            'duration': dialog.duration(),
            'is_incoming': True,
            'info': info,
            'filename': os.path.basename(filename),
        }
