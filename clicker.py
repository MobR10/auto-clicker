import time
import keyboard as kb
import threading
from pynput.keyboard import Key, Listener

# PRESS AND RELEASE LOOP
press_release_hold=False
press_release_hold_enable_button='h'
press_release_hold_toggle_button='q'

# ONE PRESS AND HOLD
one_press_hold=False
one_press_hold_enable_button='j'
one_press_hold_toggle_button='q'

# EXIT BUTTON
exit_button='+'
print(f"Press {press_release_hold_enable_button.capitalize()} to keep pressing and releasing {press_release_hold_toggle_button.capitalize()}!\n")  
print(f"Press {one_press_hold_enable_button.capitalize()} to keep pressing {one_press_hold_toggle_button.capitalize()}!\n")
print(f"Press {exit_button.capitalize()} to exit the program!\n")


def clicker():
    global press_release_hold
    while press_release_hold:
        kb.press_and_release(press_release_hold_toggle_button)
        time.sleep(0.03)
    kb.release(press_release_hold_toggle_button)
    print("PRESS RELEASE HOLD OFF\n")

def main_program(key):
    global one_press_hold,press_release_hold
    try:
        # PRESS RELEASE HOLD
        if key.char==press_release_hold_enable_button:
            press_release_hold= not press_release_hold
            if press_release_hold:
                x=threading.Thread(target=clicker,args=())   
                x.start()
                print("PRESS RELEASE HOLD ON\n")
        # ONE PRESS HOLD
        elif key.char==one_press_hold_enable_button:
                one_press_hold=not one_press_hold
                if one_press_hold:
                    kb.press(one_press_hold_toggle_button)
                    print("ONE PRESS HOLD ON\n")
                if not one_press_hold:
                    kb.release(one_press_hold_toggle_button)
                    print("ONE PRESS HOLD OFF\n")
        # EXITING PROGRAM
        elif key.char==exit_button:
            one_press_hold=False
            press_release_hold=False
            print("EXIT")
            return False
    except AttributeError:
        pass

with Listener(on_press=main_program) as listener:
    listener.join()
    
    