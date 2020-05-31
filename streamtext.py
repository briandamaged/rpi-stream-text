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
        if line == "":
            yield "   ~~~   "
        else:
            yield line


class LineTracking(object):
    def __init__(self, line, pos):
        self.line = line
        self.pos = pos
        self.ending = False
        self.ended = False



class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./BPdots.bdf")
        textColor = graphics.Color(255, 255, 255)

        space_width = graphics.DrawText(offscreen_canvas, font, 0, 1, textColor, " ")
        horizon = offscreen_canvas.width + space_width


        line_iter = each_line(sys.stdin)
        trackings = []

        def prepare_next_line():
            try:
                line = next(line_iter)
            except StopIteration:
                pass
            else:
                trackings.append(LineTracking(line, horizon))

        prepare_next_line()

        while len(trackings) > 0:
            start_time = time.time()
            offscreen_canvas.Clear()

            for t in trackings:
                length = graphics.DrawText(offscreen_canvas, font, t.pos, 24, textColor, t.line)
                t.pos -= 1
                edge = t.pos + length

                if t.ending == False:
                    if edge <= offscreen_canvas.width:
                        t.ending = True
                        prepare_next_line()
                else:
                    if edge < 0:
                        t.ended = True
            
            trackings = filter(lambda t: not t.ended, trackings)

            latency = time.time() - start_time
            delay = max(0.008 - latency, 0.001)
            time.sleep(delay)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
