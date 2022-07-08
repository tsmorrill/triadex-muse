import random
import time
from pyo import Sine, Server


class Clock:
    def __init__(self):
        self.val = 0

    def __str__(self):
        return str(self.val)

    def pulse(self):
        self.val += 1

    def reset(self):
        self.val = 0


timer = Clock()  # one instance shared between all other objects
# this could really just be a counter variable in the main loop


class Stack:
    def __init__(self, length):
        self.length = length
        self.items = [random.randint(0, 1) for i in range(self.length)]

    def __str__(self):
        return str(self.items)

    def pulse(self, item):
        # trigger shift register
        self.items.insert(0, item)
        self.items.pop()


class BinaryCounter:
    def __init__(self, length, clock=timer):
        self.length = length
        self.digits = [0 for i in range(length)]
        self.clock = clock

    def __str__(self):
        return str(self.digits)

    def pulse(self):
        length = self.length  # for convenience

        # detect overflow?
        if sum(self.digits) == length:
            self.digits = [0 for i in range(length)]
        else:
            for location in range(len(self.digits)):
                if self.clock.val % (2**location) == 0:
                    self.digits[location] = 1 - self.digits[location]
                else:
                    pass


class TripleCounter:
    def __init__(self, length, clock=timer):
        self.length = length
        self.digits = [0 for i in range(length)]
        self.clock = clock

    def __str__(self):
        return str(self.digits)

    def pulse(self):
        # reset if everything is 1
        for location in range(len(self.digits)):
            if self.clock.val % (3 * (location + 1)) == 0:
                self.digits[location] = 1 - self.digits[location]
            else:
                pass


shiftRegister = Stack(31)
counter1 = BinaryCounter(5)
counter2 = TripleCounter(2)


class Slider:
    def __init__(
        self, val=0, binaryCounter=counter1, tripleCounter=counter2, stack=shiftRegister
    ):
        # binaryCounter and stack are what the sliders will pull values from
        self.val = val
        self.binaryCounter = binaryCounter
        self.tripleCounter = tripleCounter
        self.stack = stack

    def __str__(self):
        return str(self.val)

    def output(self):
        outputList = [0, 1]  # off, on
        for i in self.binaryCounter.digits:
            outputList.append(i)
        for i in self.tripleCounter.digits:
            outputList.append(i)
        for i in self.stack.items:
            outputList.append(i)
        return outputList[self.val]


def getNoteNum(inputList):
    """Return a scale degree."""
    # inputList should be binary, a list of the values of A through D sliders
    num, exponent = 0, 0
    for i in inputList:
        num += i * (2**exponent)
        exponent += 1
    return num


A = Slider()
B = Slider()
C = Slider()
D = Slider()
W = Slider()
X = Slider()
Y = Slider()
Z = Slider()

allSliders = [A, B, C, D, W, X, Y, Z]


def pulseAll(
    root_hz,
    sliderList=allSliders,
    stack=shiftRegister,
    clock=timer,
    binaryCounter=counter1,
    tripleCounter=counter2,
):
    """Pulse everything and return a frequency in Hz."""
    a, b, c, d, w, x, y, z = (slider.output() for slider in sliderList)

    clock.pulse()
    counter1.pulse()
    counter2.pulse()

    stack.pulse((w + x + y + z) % 2)

    intervals = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 24]
    scale_degree = 8*d + 4*c + 2*b + a
    half_step_ratio = 1.05946882217
    noteFrequency = root_hz * half_step_ratio ** intervals[scale_degree]
    print(scale_degree)
    return noteFrequency


""" User-operated variables """

# interval sliders
A.val = 17
B.val = 17
C.val = 18
D.val = 19

# theme sliders
W.val = 4
X.val = 19
Y.val = 8
Z.val = 25

root_hz = 261.6

# tempo in beats per minute
bpm = 240

""" End of user-operated variables """

# sound

seconds = 60.0 / bpm

s = Server().boot()  # booting pyo server
s.start()

while True:
    note = Sine(freq=pulseAll(root_hz=root_hz), mul=0.05).out()
    time.sleep(seconds)
