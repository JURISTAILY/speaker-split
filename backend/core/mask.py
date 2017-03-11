import functools
import itertools

class Mask:
    def __init__(self, *, mask, frame_duration):
        # mask true when the frame is speech
        self.raw_mask = mask
        self.mask = Mask.__smoothing(mask)
        assert len(self.mask) == len(self.raw_mask)
        self.frame_duration = frame_duration
        self.delta = self.frame_duration / 1000

    def __str__(self):
        return str(self.mask)

    @staticmethod
    def __compress(array):
        current = False
        counter = 0
        result = []
        for itm in array:
            if itm != current:
                result.append(counter)
                counter = 1
                current = itm
            else:
                counter += 1
        result.append(counter)
        return result

    @staticmethod
    def __uncompress(array):
        result = []
        cur = False
        for i in array:
            while i:
                result.append(cur)
                i -= 1
            cur = not cur
        return result

    @staticmethod
    def __smooth(array, radius=10):
        presum = 0
        result = []
        l = len(array)
        i = 0
        while i < l:
            itm = array[i]
            if itm < radius:
                if len(result) > 1:
                    result[-1] += itm
                    i += 1
                    if i < l:
                        result[-1] += array[i]
                else:
                    presum += itm
                    i += 1
                    if i < l:
                        presum += array[i]
            else:
                result.append(itm + presum)
                presum = 0
            i += 1
        if presum:
            result.append(presum)
        return result

    @staticmethod
    def __smoothing(array):
        return Mask.__uncompress(Mask.__smooth(Mask.__compress(array)))

    @functools.lru_cache()
    def _count_silence_frames(self):
        return self.mask.count(False)

    def _count_speech_frames(self):
        return len(self.mask) - self._count_silence_frames()

    @property
    def silence_duration(self):
        return self._count_silence_frames() * self.delta

    @property
    def silence_to_total_ratio(self):
        return self._count_silence_frames() / len(self.mask)

    @functools.lru_cache()
    def count_segments(self):
        return [(value, sum(1 for _ in group))
                for value, group in itertools.groupby(self.mask)]

    @property
    def longest_silence_segment_duration(self):
        count = max(v[1] for v in self.count_segments() if v[0])
        return count * self.delta

    @property
    def longest_speech_segment_duration(self):
        count = max(v[1] for v in self.count_segments() if not v[0])
        return count * self.delta

    @property
    def segments_amount(self):
        return len([value for value, group in itertools.groupby(self.mask) if value])

    # boolean and for mask vectors for argument
    @classmethod
    def intersect(cls, first, second):
        assert first.frame_duration == second.frame_duration
        assert len(first.mask) == len(second.mask)

        return cls(mask=[a or b for a, b in zip(first.mask, second.mask)],
                   frame_duration=first.frame_duration)

    @property
    def speech_duration(self):
        return self._count_speech_frames() * self.delta

    @property
    def speech_to_total_ratio(self):
        return self._count_speech_frames() / len(self.mask)

    def frames_to_ratio(self, frames_count):
        return frames_count / len(self.mask)

    def frames_to_duration(self, frames_count):
        return frames_count * self.delta