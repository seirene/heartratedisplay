from __future__ import division
import matplotlib as mpl
# Set correct backend
mpl.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import itertools
import threading
import time
import mplcursors
import sys
from hrm import *
from matplotlib.widgets import Button

# Polar H6
macAddress = "00:22:D0:AE:60:06"
fps = 25

class PulseFunction(object):
    startX = 0
    endX = 0.2
    pHeight = 0.9

    """Returns pulse function values for values between 0-1"""
    def __init__(self):
        super(PulseFunction, self).__init__()

    def getValue(self, x):
        topX = (self.endX - self.startX) / 4
        bottomX = 3 * (self.endX - self.startX) / 4
        func = lambda x: 0
        if x <= topX:
            func = self.pUp
        elif x <= bottomX:
            func = self.pDown
        elif x <= self.endX:
            func = self.toZero
        return func(x)

    def pUp(self, x):
        topX = (self.endX - self.startX) / 4
        a = self.pHeight / (topX - self.startX)
        return a * x

    def pDown(self, x):
        topX = (self.endX - self.startX) / 4
        bottomX = 3 * (self.endX - self.startX) / 4
        a = - 2 * self.pHeight / (bottomX - topX)
        return a * (x - topX) + self.pHeight


    def toZero(self, x):
        bottomX = 3 * (self.endX - self.startX) / 4
        a = self.pHeight / (self.endX - bottomX)
        return a * (x - bottomX) - self.pHeight


class PulseCurve(object):
    pulseFunction = None
    pulseTime = 0
    # Figure width in pixels
    figWidth = 320
    # Current pixels from left
    t = 0
    # Current position in curve of a single pulse
    i = 0
    pulse = 0
    ys = None
    # width in px for pulse 60
    pulse60Width = 100
    # time between pulses in milliseconds
    pulse60Time = 1000
    msBetweenPixels = pulse60Time / pulse60Width
    pixelsInIteration = int(pulse60Width / fps)

    """docstring for Pulse"""
    def __init__(self):
        super(PulseCurve, self).__init__()
        self.pulseFunction = PulseFunction()
        self.ys = np.zeros(self.figWidth, dtype=float)

    def setPulse(self, newPulse):
        self.pulse = newPulse

    def update(self):
        if self.pulse == 0:
            # Default time for flat line
            self.pulseTime = self.pulse60Time
        else:
            self.pulseTime = np.round(self.pulse60Time * 60 / self.pulse)

    def getData(self):
        if self.i >= self.pulseTime:
            self.update();
            self.i = 0
        for j in np.arange(0, self.pixelsInIteration):
            # how many % of pulse has been drawn
            v = self.i / self.pulseTime
            if self.pulse == 0 or v >= 1:
                val = 0
            else:
                val = self.pulseFunction.getValue(v)
            self.ys[(self.t + j) % self.figWidth] = val
            self.i += self.msBetweenPixels

        self.t += self.pixelsInIteration
        self.t = self.t % self.figWidth

        return self.ys

class PulseThread(threading.Thread):
    def __init__(self):
        super(PulseThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        hrm = Hrm(macAddress)
        while not self.stopped():
            hrm.peripheral.waitForNotifications(1.0)
            p = hrm.getPulse()
            pc.setPulse(p)

pulseThread = PulseThread()
pulseThread.start()

# Hide toolbar
mpl.rcParams['toolbar'] = 'None'

pc = PulseCurve()
fig = plt.figure(facecolor='black')
ax = fig.add_subplot(111, xlim=(0, pc.figWidth), ylim=(-1, 1), facecolor='black')

# Add pulse label to right top corner
text = ax.text(pc.figWidth - 5, 0.9, "0", color='g', fontsize=24, ha='right')

# No margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
linecolor = 'g'
linewidth = 3
line1, = ax.plot(np.arange(0, pc.figWidth), np.zeros(pc.figWidth), linecolor, linewidth=linewidth)
line2, = ax.plot(np.arange(0, pc.figWidth), np.zeros(pc.figWidth), linecolor, linewidth=linewidth)
xs = np.arange(0, pc.figWidth, 1)
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

def animate(j):
    ys = pc.getData()
    text.set_text(pc.pulse)

    if pc.pulse >= 90:
        linecolor = 'r'
    elif pc.pulse >= 80:
        linecolor = 'y'
    else:
        linecolor = 'g'

    line1.set_color(linecolor)
    line2.set_color(linecolor)
    text.set_color(linecolor)

    gapwidth = 10
    line1.set_xdata(xs[:pc.t])
    line1.set_ydata(ys[:pc.t])
    line2.set_xdata(xs[pc.t+gapwidth:])
    line2.set_ydata(ys[pc.t+gapwidth:])
    return line1,line2,text

def closeAll(args):
    pulseThread.stop()
    plt.close('all')
    sys.exit(0)

ani = animation.FuncAnimation(fig, animate, None,
                              interval=1000/fps, blit=True)

# Add close button to top left corner
buttonAxes = plt.axes([0, 0.9, 0.1, 0.1])
closeButton = Button(buttonAxes, 'Close', color='black')
closeButton.on_clicked(closeAll)

plt.show()

# Save animation to file
# Writer = animation.writers['ffmpeg']
# writer = Writer(metadata=dict(artist='irne'), fps=25)
# ani.save("pulse.mp4", writer=writer)
