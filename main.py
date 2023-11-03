import _thread
import vectoros
from time import sleep

import machine
user_button = machine.Pin(19, machine.Pin.IN)
if not user_button.value():
    print("Dupa 123")
    vectoros.run()
else:
    #import vectorscope
    #v = vectorscope.Vectorscope()
    print("Kupa")
    from screentest import *
    keyboardcb.KeyboardCB.run(100)
    main()






