#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

import sys


def each_line(fin):
    for line in fin:
        line = unicode(line.rstrip(), errors = 'ignore')
        print(line)
        yield line

def each_word(line):
    for w in line.split():
        yield w


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./BPdots.bdf")
        textColor = graphics.Color(0, 255, 255)

        def centered(message, color = textColor):
            msg_width = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width, 0, color, message)
            start_x = (offscreen_canvas.width - msg_width) // 2

            graphics.DrawText(offscreen_canvas, font, start_x, 24, color, message)


        for line in each_line(sys.stdin):
            for w in each_word(line):
                offscreen_canvas.Clear()
                centered(w)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.25)

            offscreen_canvas.Clear()
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(1.00)






# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
