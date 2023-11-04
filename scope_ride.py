import machine
import screennorm
import keyboardcb
import keyleds
import vectoros
import gc
import asyncio

screen=screennorm.ScreenNorm() 

# some globals for game state
surfer_position_x=0
surfer_position_y=0
game_score=0

# buzzer is connected to one of ADC inputs - trigger it
buzzer_enabler = machine.Pin(22, machine.Pin.OUT, 1)
buzzer_gpio = machine.Pin(26, machine.Pin.OUT)

exit_flag=False

def text_overlay():
    screen.text(80,25,"Szymon")
    screen.text(40,160,"Duchniewicz")

def back(key):
    screen.jpg("wave2d_dummy.jpg")#("bluemarble.jpg")   # button A globe
    #screen.jpg("sticky_piston_studios_logo.jpg")#("bluemarble.jpg")   # button A globe
    #text_overlay()
    
def fwd(key):
    screen.jpg("pl_earth.jpg")#"wrencher.jpg")      # button B wrencher
    text_overlay()
    
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

def draw_bg():
    # draw the parallax background 
    pass

def draw_surfer():
    # draw the surfer in the middle of the screen adjusted by their position
    print("Drawing the surfer")
    screen.jpg_pos("surfer.jpg", 120+surfer_position_x*5, 120-surfer_position_y*5) 

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
    else:
        surfer_position_y += 1

def handle_joystick_down(key):
    global surfer_position_y
    # ditto
    if surfer_position_y < -3:
        print("Too low, you lose")
    else:
        surfer_position_y -= 1

def handle_joystick_right(key):
    global surfer_position_x
    # if too far right then you drop off the wave and lose
    if surfer_position_x > 3:
        print("Too far off, you lost the wave")
    else:
        surfer_position_x += 1

def handle_joystick_left(key):
    global surfer_position_x
    # if too far left then the wave gets you
    # animation of wave progressing and beep from the beeper
    if surfer_position_x < -3:
        print("Wave got you, you lose")
    else:
        surfer_position_x -= 1

async def vos_main():
    ## we need a main loop here - buttons still work as interrupts
    # put SPS logo with our names
    ## Main logic of movement and wave animation
    global exit_flag
    keys=keyboardcb.KeyboardCB({keyleds.KEY_A: back,
                                keyleds.KEY_B: fwd,
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
        draw_wave()
        draw_surfer()
        buzzer_gpio.on()

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
