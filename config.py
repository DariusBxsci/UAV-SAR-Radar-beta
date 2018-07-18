RADAR_OBJ = None

def parse_config(filename):
    #make a dictionary to store configurations
    return

def radar_setup():
    # Get the user settings
    RADAR_OBJ.read_config_file()
    # Connect to the radar
    RADAR_OBJ.connect()
    # Get current radar configuration
    RADAR_OBJ.get_radar_config()
    # Set and get radar configuration
    RADAR_OBJ.set_radar_config()

#these functions define our configuration presets
def quick():
    radar_setup()
    RADAR_OBJ.quick_look()
    return parse_config("./config/quick.cfg")

def collect():
    radar_setup(parse_config("./config/collect.cfg"))
    RADAR_OBJ.collect()
    return parse_config("./config/quick.cfg")

#config_presets = {"quick": quick, "collect": collect}

def configure(arg):
    #evaluate the preset config function for whatever argument we got
        eval(arg[0]+"()")
