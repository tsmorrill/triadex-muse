# Triadex Muse Simulator

Simulate the 1971 Triadex Muse by Ed Fredkin and Marvin Minsky.

## Operation

Each of the eight parameters `a`, `b`, `c`, `d`, `w`, `x`, `y`, and `z` specifies the address of a single bit in the system's memory. On each loop, the `out` bits at addresses `a`, `b`, `c`, and `d` form a 4-bit number, which looks up a note from the major scale and sends it to be played by the pyo server. All bits of the shift register are moved to the right. The `feed` bits at addresses `w`, `x`, `y`, and `z` are summed modulo 2 and fed back in to the register.

These parameters are referenced in the script as `out_a`, ..., `feed_w`, ..., for convinience. Memory locations are as follows:

| Address | Contents                                |
|---------|-----------------------------------------|
| 0       | constant 0                              |
| 1       | constant 1                              |
| 2-32    | bits of the shift register              |
| 33-37   | bits of the time counter, reverse order |
| 38      | alternates 0-1 each three clock cycles  |
| 39      | alternates 0-1 each six clock cycles    |

Memory bits are written to the console for visual effect.

## Acknowledgements

Original Python code by Miles Steele (https://milessteele.com/), who acknowledges the following contributors:

Logic from descriptions by Lenny Foner (http://bella.media.mit.edu/people/foner/) and Paul Geffen (http://trovar.com/index.html).

Archived documentation of the "Triadex Muse Simulator", available here: http://web.archive.org/web/20011118181946/http://richter.simplenet.com/muse/musespec.html.

Guidance from Donald Derek Haddad (https://donaldderek.com/).
