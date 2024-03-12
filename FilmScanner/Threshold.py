new_lower_threshold_value=0
new_shutter_speed_value=0

def on_startup_threshold_trackbar(val):
    global new_lower_threshold_value
    new_lower_threshold_value=val
    pass

def on_startup_shutter_speed_trackbar(val):
    global new_shutter_speed_value
    new_shutter_speed_value=val