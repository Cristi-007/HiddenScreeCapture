import libraries as lib

def get_config_settings(configFile):
    try:
        if len(configFile.options("Configuration Settings")) != 0:
            configSettings = dict(configFile.items("Configuration Settings"))
            # Validating settings data and cast data from strings
            match(configSettings.get('capture_interval').isnumeric()):
                case True:
                    configSettings.update({"capture_interval": int(configSettings.get("capture_interval"))})
                    #-------
                    match(configSettings.get('mouse_movement_interval').isnumeric()):
                        case True:
                            configSettings.update({"mouse_movement_interval": int(configSettings.get("mouse_movement_interval"))})
                            #-------
                            match(lib.os.path.exists(configSettings.get('output_directory'))):
                                case True:
                                    return configSettings
                                case False:
                                    lib.fileHandle.custom_logging("'output_directory' key does not exist, will be used default location.", "info")
                                    configSettings.update({"output_directory":lib.os.getcwd() + "\\screenshots"})
                                    return configSettings
                        case False:
                            return " 'mouse_movement_interval' key is not numeric."  
                case False:
                    return " 'capture_interval' key is not numeric."                              
        else:
            return "No configuraton settings has been added. Please check configuration file."
        
    except (AttributeError, AttributeError, Exception) as err:
        match (err.__traceback__.tb_lineno):
            case 8:
                error = f"{err} (No 'capture_interval' setted. Will be set a default value)"
                configSettings.update({"capture_interval": 60})
            case 13:
                error = f"{err} (No 'mouse_movement_interval' setted. Will be set a default value)"
                configSettings.update({"mouse_movement_interval": 60})
            case 16:
                error = f"{err} (No 'output_directory' setted. Will be set a default value)"
                configSettings.update({"output_directory": lib.os.getcwd() + "\\screenshots"} )
             
        lib.fileHandle.custom_logging(error, 'error')