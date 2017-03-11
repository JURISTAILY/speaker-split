from enum import IntEnum
import tempfile

from .utils import stereo_to_two_mono
from .track import Track
from .mask import Mask


class SpeechState(IntEnum):
    OPERATOR = 1
    CLIENT = 2
    SILENCE = 0
    INTERRUPTION = 3

    @staticmethod
    def fromMasks(cl, op):
        if op and cl:
            return SpeechState.INTERRUPTION
        if op:
            return SpeechState.OPERATOR
        if cl:
            return SpeechState.CLIENT
        return SpeechState.SILENCE


class Dialog:
    def __init__(self, filename, *, freezing_limit=5, vad_agressiviness_level=3,
                 frame_duration=30):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.filename = filename
        file_client, file_operator = stereo_to_two_mono(self.filename,
                                                        temp_dir=self.temp_dir_obj.name)

        self.track_client = Track(file_client)
        self.track_operator = Track(file_operator)
        assert len(self.track_client) == len(self.track_operator)

        self.mask_client, self.mask_operator = (
            self.track_client.get_mask(vad_agressiviness_level, frame_duration),
            self.track_operator.get_mask(vad_agressiviness_level, frame_duration)
        )
        self.mask_both = Mask.intersect(self.mask_client, self.mask_operator)

        self.freezing_limit = freezing_limit

    def frames_to_ratio(self, frames_count):
        return self.mask_client.frames_to_ratio(frames_count)

    def frames_to_duration(self, frames_count):
        return self.mask_client.frames_to_duration(frames_count)

    def get_silence_info(self):
        return {
            'operator_speech_ratio': self.mask_operator.speech_to_total_ratio,
            'client_speech_ratio': self.mask_client  .speech_to_total_ratio,
            'operator_speech_duration': self.mask_operator.speech_duration,
            'client_speech_duration': self.mask_client  .speech_duration,

            'operator_to_client_speech_ratio':
                self.mask_operator.speech_duration / self.mask_client.speech_duration,

            'operator_longest_speech_segment_duration':
                self.mask_operator.longest_speech_segment_duration,
            'client_longest_speech_segment_duration':
                self.mask_client.longest_speech_segment_duration,

            'operator_silence_ratio': self.mask_operator.silence_to_total_ratio,
            'client_silence_ratio': self.mask_client.silence_to_total_ratio,
            'both_silence_ratio': self.mask_both.silence_to_total_ratio,

            'operator_silence_duration': self.mask_operator.silence_duration,
            'client_silence_duration': self.mask_client.silence_duration,
            'both_silence_duration': self.mask_both.silence_duration,

            'operator_longest_silence_segment_duration':
                self.mask_operator.longest_silence_segment_duration,
            'client_longest_silence_segment_duration':
                self.mask_client.longest_silence_segment_duration,
            'both_longest_silence_segment_duration':
                self.mask_both.longest_silence_segment_duration,
        }

    def duration(self):
        return self.track_client.duration

    def influence_iterator(self):
        cur = SpeechState.fromMasks(self.mask_client.mask[0], self.mask_operator.mask[0])
        prev = SpeechState.SILENCE
        duration = 0
        for cl, op in zip(self.mask_client.mask, self.mask_operator.mask):
            if cur != SpeechState.fromMasks(cl, op):
                if duration:
                    yield cur, prev, duration
                prev = cur
                cur = SpeechState.fromMasks(cl, op)
                duration = 1
            else:
                duration += 1
        yield cur, prev, duration

    def get_influence_array(self):
        return [(i[0], i[2]) for i in self.influence_iterator()]

    def transcript(self):
        return {
            'client': self.track_client.transcript(),
            'operator': self.track_operator.transcript(),
        }

    def get_interruptions_info(self):
        client = 0
        operator = 0
        both = 0
        clientFrames = 0
        operatorFrames = 0
        bothFrames = 0
        client_freezing = 0
        operator_freezing = 0
        for interruption in self.influence_iterator():
            if interruption[0] is SpeechState.INTERRUPTION:
                if interruption[1] is SpeechState.CLIENT:
                    operator += 1
                    operatorFrames += interruption[2]
                elif interruption[1] is SpeechState.OPERATOR:
                    client += 1
                    clientFrames += interruption[2]
                both += 1
                bothFrames += interruption[2]
            elif interruption[0] is SpeechState.SILENCE:
                dur = self.frames_to_duration(interruption[2])
                if interruption[1] is SpeechState.CLIENT \
                        or interruption[1] is SpeechState.INTERRUPTION:
                    if dur > self.freezing_limit:
                        operator_freezing += dur
                if interruption[1] is SpeechState.OPERATOR \
                        or interruption[1] is SpeechState.INTERRUPTION:
                    if dur > self.freezing_limit:
                        client_freezing += dur

        return {
            'operator_freezing_duration': operator_freezing,
            'client_freezing_duration': client_freezing,

            'operator_interruptions_ratio': self.frames_to_ratio(operatorFrames),
            'client_interruptions_ratio': self.frames_to_ratio(clientFrames),
            'both_interruptions_ratio': self.frames_to_ratio(bothFrames),

            'operator_interruptions_duration': self.frames_to_duration(operatorFrames),
            'client_interruptions_duration': self.frames_to_duration(clientFrames),
            'both_interruptions_duration': self.frames_to_duration(bothFrames),

            'operator_interruptions_count': operator,
            'client_interruptions_count': client,
            'both_interruptions_count': both,
        }
