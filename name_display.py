import screennorm
import keyboardcb
import keyleds
import vectoros
import gc
import asyncio

screen=screennorm.ScreenNorm() 


exit_flag=False

def text_overlay():
    screen.text(80,25,"Jakub")
    screen.text(40,160,"Duchniewicz")

def back(key):
    idx = 1
    while True:
        if idx >= 11:
            idx = 1
        path = "img/sps_" + str(idx) + ".jpg"
        screen.jpg(path)  # button A globe
        #text_overlay()
        idx += 1
        asyncio.sleep_ms(20)
    
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
    keys=keyboardcb.KeyboardCB({keyleds.KEY_A: back, keyleds.KEY_B: back, keyleds.KEY_C: stoplcd, keyleds.KEY_D: startlcd,
                                keyleds.KEY_MENU: menu})
    back(None)
    while exit_flag==False:
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