from pynput import keyboard
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import os
import threading
import time
print("<===================================>")
print("[1/3] Imported successfully")

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

print("[2/3] Loaded speaker successfully")

key_held = False

def adjust_volume_continuous(step_function):
    while key_held:
        step_function()
        time.sleep(0.05)

def volume_step_up():
    volume.VolumeStepUp(None)

def volume_step_down():
    volume.VolumeStepDown(None)

def on_press(key):
    global key_held
    try:
        if key == keyboard.Key.media_volume_up:
            if not key_held:
                key_held = True
                threading.Thread(target=adjust_volume_continuous, args=(volume_step_up,)).start()
                print('[+] Going up')
        elif key == keyboard.Key.media_volume_down:
            if not key_held:
                key_held = True
                threading.Thread(target=adjust_volume_continuous, args=(volume_step_down,)).start()
                print('[-] Going down')
    except AttributeError as e:
        print('[!] ' + e)
        pass

def on_release(key):
    global key_held
    if key == keyboard.Key.esc:
        return False
    if key == keyboard.Key.media_volume_up or key == keyboard.Key.media_volume_down:
        key_held = False
print("[3/3] Code initialized succesfully")
print("<===================================>")
print("")
print("[?] Holding volume keys will only print once")
print("[>] Press ESC to exit")
print("")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
