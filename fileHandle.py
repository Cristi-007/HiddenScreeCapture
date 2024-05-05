import libraries as lib


# Open config file and parse data from it
def read_config_file():
    try:
        # Check if file exists, if not - getting error and move to exception
        f = open(lib.os.getcwd() + "\\config.ini", "r")
        f.close()

        # Read config file
        configFile = lib.configparser.ConfigParser()
        configFile.read(lib.os.getcwd() + "\\config.ini")

        # Parse data from config file
        if configFile.has_section("Configuration Settings"):
            data = lib.SettProc.get_config_settings(configFile)
            if type(data) is not dict:
                custom_logging(f"Error: encountered following problems - {data}!", "error")
                exit()
            else:
                custom_logging(f"All settings has been set! Continue....")
                return data
        else:
            custom_logging(f"No Configuration Settings set. Program Stopped.", "error")
            exit()
    except IOError:
        custom_logging("Config file does not exist or it is not readable! It will be created and used with default values.", 'info')
        
        configSettings = dict({
            "output_directory": lib.os.getcwd() + "\\screenshots",
            "capture_interval": 60,
            "mouse_movement_interval": 60,
            "file_settings": {
                    "file_name": "config.ini",
                    "file_type": "config",
                    "file_operation": "w"
                }
        })

        if lib.os.path.exists(f"{lib.os.getcwd()}\\screenshots") != True:
            lib.os.mkdir(f"{lib.os.getcwd()}\\screenshots")
        
        create_config_file(configSettings)
        return configSettings



def create_config_file(data):
    try:
        match (data["file_settings"].get("file_type")):
            case "config":
                dataFile = lib.configparser.ConfigParser(allow_no_value=True)
                dataFile.add_section('Configuration Settings')
                
                for i in data:
                    if i == "file_settings":
                        break
                    dataFile.set("Configuration Settings", i, str(data[i]))
                 
                with open(lib.os.getcwd() + '\\' + data["file_settings"]["file_name"], data["file_settings"]["file_operation"]) as file:
                    file.write("# Settings has been set with default values. Please change them as you want.\n\n")
                    dataFile.write(file)
            case _:
                pass                
    except IOError as error:
        custom_logging(error, 'critical')
        exit()
        


def custom_logging(message, level='info'):
# Is it a good aproach of this method ????
    if lib.os.path.exists(f"{lib.os.getcwd()}\\logs") != True:
        lib.os.mkdir(f"{lib.os.getcwd()}\\logs")
        
    file_path = f"{lib.os.getcwd()}\\logs\\{str(lib.datetime.datetime.now().strftime('%d_%m_%Y'))}.log"
    
    #Create the logger and file handler once pe application
    if not getattr(custom_logging, 'logger', None):
        # Set up the logger with a custom formatter
        formatter = lib.logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%H:%M:%S")
        
        # Create a logger
        logger = lib.logging.getLogger(__name__)
        logger.setLevel(lib.logging.DEBUG)

        # Create a file handler if file_path is provided
        file_handler = lib.logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Store the logger
        custom_logging.logger = logger
        
    # Get the log function based on the specified level
    log_func = getattr(custom_logging.logger, level.lower(), custom_logging.logger.info)
    
    # Log the message
    log_func(message)





def create_shotcut_to_startup():
    try:
        startupPath = lib.os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
        applicationName = lib.os.path.basename(lib.sys.executable)[:-4]

        shell = lib.win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(f'{startupPath}\\{applicationName}.lnk')
        shortcut.IconLocation = lib.sys.executable
        shortcut.Targetpath = lib.sys.executable
        shortcut.WorkingDirectory = lib.os.getcwd()
        shortcut.save()

        lib.fileHandle.custom_logging('Succesfully saved shotcut for autostart.', 'info')
        
        # dar daca home la user este pe D: ?????
    except Exception as err:
        lib.fileHandle.custom_logging(err, 'error')
    
