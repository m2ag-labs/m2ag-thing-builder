import multiprocessing
import time

import board
import neopixel
import zerorpc

# https://learn.adafruit.com/circuitpython-led-animations/basic-animations
# https://circuitpython.readthedocs.io/projects/neopixel/en/latest/api.html
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
# https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
# https://dzone.com/articles/python-thread-part-1


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 1
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=True, pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        time.sleep(wait)


def run(mode):
    while True:
        rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step


class NeoRPC(object):
    def __init__(self):
        self.process = None
        pixels.fill((0, 0, 0))

    def mode(self, value):

        if 'brightness' in value:
            pixels.brightness = value['brightness'] / 100
            return pixels.brightness * 100

        if 'pattern' in value:
            pattern = value['pattern']

            if self.process is not None:
                self.process.terminate()
                self.process = None

            if pattern < 7:
                if pattern == 0:  # off
                    pixels.fill((0, 0, 0))
                if pattern == 1:  # green
                    pixels.fill((30, 228, 6))
                if pattern == 2:  # yellow
                    pixels.fill((255, 255, 10))
                if pattern == 3:  # Orange
                    pixels.fill((253, 104, 10))
                if pattern == 4:  # Red
                    pixels.fill((251, 0, 7))
                if pattern == 5:  # purple
                    pixels.fill((123, 40, 133))
                if pattern == 6:  # magenta
                    pixels.fill((106, 0, 27))
            else:
                if pattern == 7:
                    self.process = multiprocessing.Process(target=run, args=(pattern,))
                    self.process.start()
            return pattern


s = zerorpc.Server(NeoRPC())
s.bind("tcp://127.0.0.1:4242")
s.run()
