import libraries as lib


class globalVariables:
    def __init__(self, mousePos):
        self.mousePos = mousePos

def main():
    try:      
        instance = lib.singleton.SingleInstance() # will sys.exit(-1) if other instance is running
        logFlag = 0
        
        lib.fileHandle.custom_logging('Program has started with PID: ' + str(lib.os.getpid()) + ' and PPID: ' + str(lib.os.getppid()),'info')
        lib.fileHandle.create_shotcut_to_startup()
         
        configSettings = lib.fileHandle.read_config_file()
        initialMousePosition = globalVariables(lib.mouse.get_position())
        lib.userActiveCheck.user_logon_check()
        lib.keyboard.start_recording()
                
        lib.schedule.every(configSettings.get("capture_interval")).seconds.do(lib.function.take_screenshot, configSettings.get("output_directory"))
        lib.schedule.every(configSettings.get("mouse_movement_interval")).seconds.do(lib.userActiveCheck.mouse_movement_check, initialMousePosition)
        
        while True:
            rdpConnected = lib.function.rdp_connected()
            
            if rdpConnected is True:
                lib.schedule.run_pending()
                if logFlag == 0:
                    logFlag = 1
                    lib.fileHandle.custom_logging('Connected via RDP ...', 'info')
            else:
                lib.userActiveCheck.user_logon_check()
                lib.schedule.run_pending()
                if logFlag == 1:
                    logFlag = 0
                    lib.fileHandle.custom_logging('RDP connection closed.', 'info') 
        
    except Exception as err: 
        lib.fileHandle.custom_logging(err, 'error')
    
if __name__ == '__main__':
    main()