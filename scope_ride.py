import machine
import screennorm
import keyboardcb
import keyleds
import vectoros
import gc
import asyncio
#from img_bitmaps import SURFER_BITMAP
import surfer_bitmap
import wave_bitmap
import framebuf

screen: screennorm.ScreenNorm =screennorm.ScreenNorm() 

# some globals for game state
surfer_position_x=0
surfer_position_y=0
game_score=0
lost_life = False
bg_scroll_position=0

from buzzer_music import music

# TODO: replace with surfing USA and make it slightly less loud
# add mute button
#    https://onlinesequencer.net/1140127 C418 - Sweden
surfing_song = '64 E3 4 13;64 E4 4 13;64 G4 4 13;64 B4 4 13;68 F#3 4 13;76 B3 4 13;80 A3 4 13;84 G3 4 13;88 D3 4 13;72 D5 4 13;72 A4 4 13;72 F#5 4 13;72 G3 4 13;80 F#4 4 13;80 A4 4 13;80 C#5 4 13;88 A4 4 13;88 C#5 4 13;88 E5 4 13;96 E3 4 13;96 E4 4 13;96 G4 4 13;96 B4 4 13;100 F#3 4 13;108 B3 4 13;112 A3 4 13;116 G3 4 13;120 D3 4 13;104 D5 4 13;104 A4 4 13;104 F#5 4 13;104 G3 4 13;112 F#4 4 13;112 A4 4 13;112 C#5 4 13;120 A4 4 13;120 C#5 4 13;120 E5 4 13;0 E3 4 13;4 F#3 4 13;12 B3 4 13;16 A3 4 13;20 G3 4 13;24 D3 4 13;8 G3 4 13;32 E3 4 13;36 F#3 4 13;44 B3 4 13;48 A3 4 13;52 G3 4 13;56 D3 4 13;40 G3 4 13;0 E4 4 13;0 G4 4 13;8 A4 4 13;8 D5 4 13;16 A4 4 13;16 F#4 4 13;24 A4 4 13;24 C#5 4 13;32 E4 4 13;32 G4 4 13;40 A4 4 13;40 D5 4 13;48 A4 4 13;48 F#4 4 13;56 A4 4 13;56 C#5 4 13;128 E3 4 13;128 E4 4 13;128 G4 4 13;128 B4 4 13;132 F#3 4 13;140 B3 4 13;144 A3 4 13;148 G3 4 13;152 D3 4 13;136 D5 4 13;136 A4 4 13;136 F#5 4 13;136 G3 4 13;144 F#4 4 13;144 A4 4 13;144 C#5 4 13;152 A4 4 13;152 C#5 4 13;152 E5 4 13;132 A5 2 13;134 B5 2 13;142 D5 1 13;143 E5 1 13;150 F#5 1 13;151 A5 1 13;160 E3 4 13;160 E4 2 13;160 G4 2 13;160 B4 2 13;164 F#3 4 13;172 B3 4 13;176 A3 4 13;180 G3 4 13;184 D3 4 13;168 D5 4 13;168 A4 4 13;168 F#5 4 13;168 G3 4 13;176 F#4 4 13;176 A4 4 13;176 C#5 4 13;184 A4 4 13;184 C#5 4 13;184 E5 4 13;162 D6 2 13;164 B5 2 13;166 A5 2 13;174 D5 1 13;175 E5 1 13;182 A5 1 13;183 F#5 1 13'
#sad_trumpet_song = 

# buzzer is connected to one of ADC inputs - trigger it
buzzer_enabler = machine.Pin(22, machine.Pin.OUT, 1)
surfing_music = music(surfing_song, pins=[machine.Pin(26)])
#sad_trumpet_music
#buzzer_gpio = machine.Pin(26, machine.Pin.OUT)
#wave_frame_bitmap = framebuf.FrameBuffer(wave_bitmap.BITMAP, wave_bitmap.WIDTH, wave_bitmap.HEIGHT, framebuf.GS2_HMSB)
#surfer_frame_bitmap = framebuf.FrameBuffer(surfer_bitmap.BITMAP, surfer_bitmap.WIDTH, surfer_bitmap.HEIGHT, framebuf.GS8)

exit_flag=False

import gc
import os
import machine


def text_overlay():
    screen.text(80,25,"Szymon")
    screen.text(40,160,"Duchniewicz")

def back(key):
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    screen.tft.pbitmap(wave_bitmap,0,0)
    #screen.tft.bitmap(wave_bitmap,0,0)
    #screen.jpg("wave2d_dummy.jpg")#("bluemarble.jpg")   # button A globe
    #screen.jpg("sticky_piston_studios_logo.jpg")#("bluemarble.jpg")   # button A globe
    #text_overlay()
    
def handle_restart(key):
    print("Restart pressed")
    restart()
    
def menu(key):						# menu -bail out
    global exit_flag
    exit_flag=True

def startlcd(key):					# button D - start LCD
    if screen.tft==None:
        screen.wake()
        back(None)

def stoplcd(key):					# button C stop LCD
    if screen.tft!=None:
        screen.clear()
        screen.idle()

def game_loop():
    # game loop works like that:
    # the surfer first needs to catch the wave?
    # then the wave will randomly try to shake the surfer off, changing the vector the surfer is pushed
    # favoring pushing back and down
    # the surfer needs to stay on the wave as long as possible
    # there will be a meter of wave score made in the HW?
    # 
    pass

# TODO: can add several life and loosing them one by one
def loose():
    # play loosing sound
    surfing_music.stop()
    lost_life = True
    
def restart():
    surfing_music.restart()
    lost_life = False

def draw_bg():
    # draw the parallax background
    global bg_scroll_position
    path = "img/background/" + str(bg_scroll_position) + ".jpg"
    screen.jpg(path)
    bg_scroll_position += 1
    # Wrap back around if beyond the last parallax image!
    if bg_scroll_position > 10:
        bg_scroll_position = 0

def draw_surfer():
    # draw the surfer in the middle of the screen adjusted by their position
    print("Drawing the surfer")
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    screen.tft.bitmap(surfer_bitmap, 120+surfer_position_x*5, 120-surfer_position_y*5)
    #screen.tft.bitmap(SURFER_BITMAP, 120+surfer_position_x*5, 120-surfer_position_y*5)
    #screen.jpg_pos("surfer.jpg", 120+surfer_position_x*5, 120-surfer_position_y*5) 

def draw_wave():
    screen.jpg("wave2d_dummy.jpg")

def handle_jump(key):
    print("Pressed jump")
    pass

def handle_joystick_up(key):
    global surfer_position_y
    # get too high, also loose
    if surfer_position_y > 3:
        print("Too high, you lose")
        loose()
    else:
        surfer_position_y += 1

def handle_joystick_down(key):
    global surfer_position_y
    # ditto
    if surfer_position_y < -3:
        print("Too low, you lose")
        loose()
    else:
        surfer_position_y -= 1

def handle_joystick_right(key):
    global surfer_position_x
    # if too far right then you drop off the wave and lose
    if surfer_position_x > 3:
        print("Too far off, you lost the wave")
        loose()
    else:
        surfer_position_x += 1

def handle_joystick_left(key):
    global surfer_position_x
    # if too far left then the wave gets you
    # animation of wave progressing and beep from the beeper
    if surfer_position_x < -3:
        print("Wave got you, you lose")
        loose()
    else:
        surfer_position_x -= 1

async def vos_main():
    ## we need a main loop here - buttons still work as interrupts
    # put SPS logo with our names
    ## Main logic of movement and wave animation
    global exit_flag
    keys=keyboardcb.KeyboardCB({keyleds.KEY_A: back,
                                keyleds.KEY_B: handle_restart,
                                keyleds.KEY_C: stoplcd, 
                                keyleds.KEY_D: startlcd,
                                keyleds.KEY_MENU: menu,
                                # for now using regular key mapped
                                keyleds.KEY_LEVEL : handle_jump,
                                keyleds.JOY_UP: handle_joystick_up,
                                keyleds.JOY_DN: handle_joystick_down,
                                keyleds.JOY_RT: handle_joystick_right,
                                keyleds.JOY_LT: handle_joystick_left})
    back(None)
    while exit_flag==False:

        # draw from back to front
        draw_bg()
        #draw_wave()
        draw_surfer()
        s = os.statvfs('/')
        print(f"Free storage: {s[0]*s[3]/1024} KB")
        print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
        #gc.collect()
        #print(f"After GC collect Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
        print(f"CPU Freq: {machine.freq()/1000000}Mhz")
        #buzzer_gpio.on()
        if lost_life:
            sad_trumpet_music.tick()
        else:
            surfing_music.tick()

        await asyncio.sleep_ms(500)
        if vectoros.vectoros_active==False:
            gc.collect()
# stop listening for keys
    keys.detach()
    exit_flag=False  # next time
    from vos_state import vos_state
    vos_state.show_menu=True
    
def main():
    asyncio.run(vos_main())


if __name__=="__main__":
    keyboardcb.KeyboardCB.run(100)
    main()
