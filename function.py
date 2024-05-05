import libraries as lib


def take_screenshot(output_directory):
    if lib.os.path.exists(f"{lib.os.getcwd()}\\screenshots") != True:
        lib.os.mkdir(f"{lib.os.getcwd()}\\screenshots")

    imageName = f"{str(lib.datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'))}"   #pregateste denumirea fisierului
    screenshot = lib.mss.mss().grab(lib.mss.mss().monitors[0])

    filePath = f"{output_directory}\\{imageName}.png"

    newImage = lib.Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    newImage.save(filePath)
    
    #print()



def rdp_connected():
    output = lib.subprocess.check_output('qwinsta', stderr=lib.subprocess.STDOUT,
                          creationflags=lib.subprocess.CREATE_NO_WINDOW).decode('latin1')
    for line in output.split('\r\n'):
        if 'rdp-tcp#' in line and 'Active' in line:
            return True
    return False
