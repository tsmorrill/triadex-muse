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


timer = Clock()


class Stack:
    # use in Muse: create with 31 bits

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
    # use in Muse: create with five bits

    def __init__(self, length, clock=timer):
        self.length = length
        self.digits = [0 for i in range(length)]
        self.clock = clock

    def __str__(self):
        return str(self.digits)

    def pulse(self):
        length = self.length  # for convenience

        def switch(digit):
            if digit == 0:
                return 1
            else:
                return 0

        # detect stuck state
        if sum(self.digits) == length:
            self.digits = [0 for i in range(length)]
        else:
            for location in range(len(self.digits)):
                if self.clock.val % (2**location) == 0:
                    self.digits[location] = switch(self.digits[location])
                else:
                    pass


class TripleCounter:
    # use in Muse: create with two bits

    def __init__(self, length, clock=timer):
        self.length = length
        self.digits = [0 for i in range(length)]
        self.clock = clock

    def __str__(self):
        return str(self.digits)

    def pulse(self):
        length = self.length  # this isn't getting used anywhere

        def switch(digit):
            if digit == 0:
                return 1
            else:
                return 0

        # now the main activity of the function
        # reset if everything is 1
        for location in range(len(self.digits)):
            if self.clock.val % (3 * (location + 1)) == 0:
                self.digits[location] = switch(self.digits[location])
            else:
                pass


shiftRegister = Stack(31)
counter1 = BinaryCounter(5)
counter2 = TripleCounter(2)


class Slider:
    # use in Muse: create 'A','B','C','D' (interval),'W','X','Y','Z' (theme) sliders

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


def parityGen(inputList):
    # inputList should be a binary, a list of the values of W through Z sliders
    summedOuts = sum(inputList)
    output = summedOuts % 2
    return output


def getNoteNum(inputList):
    """Return a scale degree."""
    # inputList should be binary, a list of the values of A through D sliders
    num, exponent = 0, 0
    for i in inputList:
        num += i * (2**exponent)
        exponent += 1
    return num


def getNoteFrequency(key, noteNum):
    # key = tonic frequency, noteNum = placement in scale (e.g. 0 = tonic, 1 = whole step up)
    # progression of half tone increases in a major scale
    halfTones = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 24]
    # convert to Hz
    frequency = key * (1.05946882217 ** halfTones[noteNum])
    return frequency


A = Slider()
B = Slider()
C = Slider()
D = Slider()
W = Slider()
X = Slider()
Y = Slider()
Z = Slider()

allSliders = [A, B, C, D, W, X, Y, Z]
pitch = 261.6


def pulseAll(
    key=pitch,
    sliderList=allSliders,
    stack=shiftRegister,
    clock=timer,
    binaryCounter=counter1,
    tripleCounter=counter2,
):
    """Pulse everything and return a frequency in Hz."""
    # sliderList is list of sliders: first four interval, last four theme
    # call all slider values
    sliderVals = []
    for slider in sliderList:
        sliderVals.append(slider.output())
    # pulse all forward
    clock.pulse()
    counter1.pulse()
    counter2.pulse()
    parityIn = [sliderVals[i + 4] for i in range(4)]
    parityOut = parityGen(parityIn)
    stack.pulse(parityOut)
    # get note, return in Hz
    noteNum = getNoteNum([sliderVals[i] for i in range(4)])
    noteFrequency = getNoteFrequency(key, noteNum)
    print(noteNum)
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

# key: middle C = 261.6
pitch = 200

# tempo in beats per minute
bpm = 240

""" End of user-operated variables """

# sound

seconds = 60.0 / bpm

s = Server().boot()  # booting pyo server
s.start()

while True:
    note = Sine(freq=pulseAll(pitch), mul=0.05).out()
    time.sleep(seconds)
