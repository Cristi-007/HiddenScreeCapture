import libraries as lib


def mouse_movement_check(initialMousePosition):
    while(True):
        newPos = lib.mouse.get_position()
        rdpConnected = lib.function.rdp_connected()
        isKeyboardPressed = keyboard_press_check()
        if newPos != initialMousePosition.mousePos or rdpConnected is True or isKeyboardPressed is True:
            break
    initialMousePosition.mousePos = newPos



def user_logon_check():
    isScreenLocked = True
    lockProcessName = 'LogonUI.exe'
    while isScreenLocked:
        taskList = str(lib.subprocess.check_output('TASKLIST', shell=True))
        rdpConnected = lib.function.rdp_connected()
        if lockProcessName not in taskList or rdpConnected is True:
            break
        

def keyboard_press_check():
    keyboardEvents = lib.keyboard.stop_recording()
    if len(keyboardEvents) == 0:
        lib.keyboard.start_recording()
        return False
    else:
        lib.keyboard.start_recording()
        return True
    
    # face 2 capturi chiar daca am apasat odata pe tasta
    #while len(keyboardEvents) == 0:
        #print(len(keyboardEvents))
        #print('test')
        #lib.keyboard.start_recording()
        #lib.time.sleep(10)
        #keyboardEvents = lib.keyboard.stop_recording()
