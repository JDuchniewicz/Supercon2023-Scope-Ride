import screennorm
import keyboardcb
import keyleds
import vectoros
import gc
import asyncio

screen=screennorm.ScreenNorm() 


exit_flag=False

def text_overlay(text="Wave rider", off=0):
    screen.text(40,25, text)
    screen.text(85,190+off,"2023")

def back(key):
    #screen.jpg("pl_mars.jpg")#("bluemarble.jpg")   # button A globe
    #text_overlay("Wave rider")
    #return
    i = 0
    inc = 1
    while True:
        screen.jpg("wave2d_dummy.jpg")#("bluemarble.jpg")   # button A globe
        if i >= 10:
            inc = -1
        elif i <= -10:
            inc = +1
        i += inc
        text_overlay("Wave rider",i)
        asyncio.sleep_ms(2)
    
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

async def vos_main():
    global exit_flag
    keys=keyboardcb.KeyboardCB({keyleds.KEY_A: back, keyleds.KEY_B: fwd, keyleds.KEY_C: stoplcd, keyleds.KEY_D: startlcd,
                                keyleds.KEY_MENU: menu})
    back(None)
    while exit_flag==False:
        await asyncio.sleep_ms(500)
        if vectoros.vectoros_active==False:
            print("Siki")
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
