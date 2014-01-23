#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TAP Lab rhythm generation (python port)

Notes to myself:
- (duration, gap) tuples go with amplitude (1, 0). so a gap is a sound with zero amplitude
- remove_click uses a hamming window, not a variable len ramp
- removed play option from MakeTone functions; just make tones
"""


import numpy as np
from numpy import zeros, linspace, random, pi, sin
from scipy.io import wavfile
from scipy.signal import sawtooth, square
from psychopy import sound, core

# for test():
import time
from matplotlib import pyplot

def play_array(stim, fs):
    """Creates a PsychoPy.sound.Sound() and plays it
    """
    s = sound.Sound(stim, sampleRate=fs)
    s.play()
    core.wait(s.getDuration())

def remove_click(stim, fs, window=5):
    """Reduce a sound's 'click' onset / offset using a Hamming window, <window> ms
    """
    hwSize = min(fs // (1000//window), len(stim) // 15)
    hammingWindow = np.hamming(2 * hwSize + 1)
    stim[:hwSize] *= hammingWindow[:hwSize]
    for i in range(2):
        stim[-hwSize:] *= hammingWindow[hwSize + 1:]

    return stim

#frequency is in hertz
#duration is in seconds
#amp is the intensity value between 0 and 1
#fs = sampling rate, typically 44100 Hz

def makeTone(freq, duration, amp, fs, toneShape):
    #  shape = scipy.signal.square, scipy.signal.sawtooth, or np.sin
    t = linspace(0, 1, fs * duration)
    tone = toneShape(freq*2*pi*t)*amp

    return tone

def makeSquareTone(freq, duration, amp, fs):
    return makeTone(freq, duration, amp, fs, square)

def makeSawTone(freq, duration, amp, fs):
    return makeTone(freq, duration, amp, fs, sawtooth)

def makeSineTone(freq, duration, amp, fs):
    return makeTone(freq, duration, amp, fs, sin)

def makeNoise(freq, duration, amp, fs):
    # white noise

    n = int(duration * fs)
    nvec = random.rand(n) * 2. - 1

    return nvec

def createRhythm(dvec, avec, freq, filename='', play=False,
                 fxn=makeSineTone, fs=44100):
    # fxn = the function to be called
    # saves as a file if a filename is provided
    # dvec durations in ms

    n1 = len(dvec)  # duration vec
    n2 = len(avec)  # amplitude vector to specific intensity of each tone
    assert n1 == n2

    sec = dvec / 1000.

    length = sum(sec) * fs
    sndvec = np.zeros(length)
    start = 0
    for i in range(n1):
        if avec[i] == 0:
            start += int(sec[i] * fs)
            continue
        stim = remove_click(fxn(freq, sec[i], avec[i], fs), fs)  # cache?
        stop = start + len(stim)
        sndvec[start:stop] = stim
        start = stop

    sndvec = sndvec * 0.99  # prevent clipping
    if play:
        play_array(sndvec, fs)
    if filename:
        w = sndvec * 2**15
        wavfile.write(filename, fs, w.astype(np.int16))
    return sndvec

def test():
    # durations in ms

    dur =  50
    gap = 200
    n = 10
    freq = 44
    dvec1 = np.array([dur, gap] * n)
    avec = np.array((1, 0) * n)
    for f in ['makeNoise', 'makeSineTone', 'makeSquareTone', 'makeSawTone']:
        fxn = eval(f)
        t0 = time.time()
        svec = createRhythm(dvec1, avec, freq, play=True, fxn=fxn, filename=f+'.wav')
        print time.time() - t0
        plot(svec, label=repr(fxn))

def plot(yaxis, label):
    pyplot.plot(range(len(yaxis)), yaxis)
    pyplot.title(label)
    pyplot.draw()
    pyplot.show()

def metronome():
    # durations in ms

    dur =  50
    gap1 = 200
    gap2 = 550
    gap3 = 1250

    filename1 = 'Pace250.wav'
    filename2 = 'Pace600.wav'
    filename3 = 'Pace1300.wav'

    n = 30
    freq = 44

    dvec1 = np.array([dur, gap1] * n)
    dvec2 = np.array([dur, gap2] * n)
    dvec3 = np.array([dur, gap3] * n)
    avec = np.array((1, 0) * n)

    createRhythm(dvec1, avec, freq, filename1, play=True, fxn=makeSineTone)
    createRhythm(dvec2, avec, freq, filename2, play=True, fxn=makeSawTone)
    createRhythm(dvec3, avec, freq, filename3, play=True, fxn=makeSquareTone)
