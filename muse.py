from random import randint
import time
from pyo import Sine, Server


def muse(out_a, out_b, out_c, out_d, feed_w, feed_x, feed_y, feed_z):
    """Emulate the Triadex Muse."""
    if (
        min(out_a, out_b, out_c, out_d, feed_w, feed_x, feed_y, feed_z) < 0
        or max(out_a, out_b, out_c, out_d, feed_w, feed_x, feed_y, feed_z) > 40
    ):
        raise ValueError("tap locations must be integers from 0 to 40.")

    shift_register = [randint(0, 1) for _ in range(31)]
    t = 0

    while True:

        constant_taps = [0, 1]
        bit_taps = [(t >> i) & 1 for i in range(5)]
        tri_taps = [int(t % 12 > 5), int(t % 6 > 3)]
        all_taps = constant_taps + shift_register + bit_taps + tri_taps

        scale_degree = (
            8 * all_taps[out_d]
            + 4 * all_taps[out_c]
            + 2 * all_taps[out_b]
            + all_taps[out_a]
        )

        semitones = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 24]

        print(all_taps)
        yield semitones[scale_degree]

        bit = (
            all_taps[feed_w] + all_taps[feed_x]
            + all_taps[feed_y] + all_taps[feed_z]
        ) % 2

        shift_register.insert(0, bit)
        shift_register.pop()

        t += 1


if __name__ == "__main__":
    semitone = muse(17, 17, 18, 19, 4, 19, 8, 25)

    C_hz = 261.6
    half_step_ratio = 1.05946882217
    bpm = 240
    seconds = 60.0 / bpm

    s = Server().boot()
    s.start()

    while True:
        steps = next(semitone)
        freq = C_hz * half_step_ratio**steps
        note = Sine(freq=freq, mul=0.05).out()
        time.sleep(seconds)
