import argparse
import os
import os.path
import logging

import core
import app


parser = argparse.ArgumentParser(description='Calc parameters for new recordings.')
parser.add_argument('recordings_dir',
                    help='directory containing the recordings')


class Monitor:
    def __init__(self, path):
        self.path = path
        self.engine = core.Engine()

    def _list_recordings(self):
        return [
            f for f in os.listdir(self.path)
            if os.path.isfile(os.path.join(self.path, f))
            and (f.endswith('.wav') or f.endswith('.mp3'))
        ]

    def do(self):
        db = app.db
        Call = app.Call
        log = logging.getLogger(__name__)

        for rec in self._list_recordings():
            log.debug('-' * 79)
            log.debug('Checking file "{}"...'.format(rec))
            call = (
                db.session.query(Call)
                          .filter_by(recording_filename=rec)
                          .first()
            )
            if call:
                log.debug('Recording already processed: {}'.format(call))
                continue
            log.debug('This recording is new. Processing it...')
            try:
                data = self.engine.process_recording(os.path.join(self.path, rec))
                Call.add_new(data)
                log.debug('Recording successfully processed.')
            except Exception:
                log.exception('Could not process recording.')


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s (%(name)s) %(message)s')

    args = parser.parse_args()
    monitor = Monitor(os.path.abspath(args.recordings_dir))
    monitor.do()
    exit(0)
