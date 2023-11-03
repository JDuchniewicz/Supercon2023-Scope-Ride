from vectorscope import Vectorscope
from dds import DDS

import gc
import math
import time
from vos_debug import debug_print as debug
import vectoros
import vos_state
import vos_debug
import keyboardcb
import keyleds
import keyboardio
import asyncio

_abort=False
## map waveform types to LEDs
_waves_lookup = {0:"sine", 3:"sawtooth", 1:"square", 2:"triangle"}
_waves_reverse_lookup = {"sine":0, "sawtooth":3, "square":1, "triangle":2}

lissajous_state = {
        "selected_axis":0, 
        "selected_waveform":0,
        "waves_leds":[0,0]

        }

async def do_dds_loop(d):
    while not _abort:
        for i in range(50):
            d.do_dds()
            d.populate_buffer()
            await asyncio.sleep(0)
    
def do_abort(key):
    global _abort
    _abort=True


async def vos_main():

    vectoros.get_screen().idle()
    gc.collect()
    vos_state.gc_suspend=True
    # await asyncio.sleep(1)
    
    keyboardio.KeyboardIO.leds = (1<<7) 
    keyboardio.KeyboardIO.leds |= (1<<5) ## sine wave
    keyboardio.KeyboardIO.scan()

    v = Vectorscope()

    def static_buffer_example(v):
        ## Example of more complicated, repetitive waveform
        ## v.wave has two buffers of 256 samples for putting sample-wise data into: 
        ## v.wave.outBufferX and outBufferY.  These are packed 16 bits each, LSB first
        ## To make your life easier, v.wave.packX() will put a list of 16-bit ints there for you

        ramp = range(-2**15, 2**15, 2**8)
        v.wave.packX(ramp)

        #sine = [int(math.sin(2*x*math.pi/256)*16_000) for x in range(256)]
        sawtooth = [x for x in range(256)]
        v.wave.packY(sawtooth)

        time.sleep_ms(1000)

        ## That discontinuity and wobble is real -- 
        ##  that's what happens when you try to push around a real DAC that's bandwidth-limited.

    await static_buffer_example(v)
    
    vectoros.reset()



