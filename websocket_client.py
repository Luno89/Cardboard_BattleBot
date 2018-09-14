from lomond import WebSocket
from pynput import keyboard

speed = 0
direction = 0
websocket = WebSocket('ws://localhost:8000/')

im_ready = False

def on_press(key):
    global speed
    global direction
    try:
        if key == keyboard.KeyCode.from_char('w'):
            speed = 10
        if key == keyboard.KeyCode.from_char('s'):
            speed = -10
        if key == keyboard.KeyCode.from_char('d'):
            direction = 10
        if key == keyboard.KeyCode.from_char('a'):
            direction = -10
    except Exception:
        print( "something bad happened")

def on_release(key):
    global speed
    global direction
    if key == keyboard.KeyCode.from_char('w'):
        speed = 0
    if key == keyboard.KeyCode.from_char('s'):
        speed = 0
    if key == keyboard.KeyCode.from_char('d'):
        direction = 0
    if key == keyboard.KeyCode.from_char('a'):
        direction = 0

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    for event in websocket:
        if event.name == "ready":
            text = input("Give me something: ")
            websocket.send_text(text)
            im_ready = True
        elif event.name == "poll":
            websocket.send_text("I'm polling here")
        elif event.name == "text":
            print(event.text)
        if im_ready == True:
            websocket.send_text("{'direction':" + str(direction) + ",'speed':" + str(speed) + "}")

    listener.join()

