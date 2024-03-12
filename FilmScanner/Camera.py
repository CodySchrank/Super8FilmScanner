from picamera2 import Picamera2, Preview
import time


shutter_speed = 1000
iso = 50

camera = None

# def AutoShutterSpeed(c: PiCamera):
#     c.exposure_mode = 'auto'
#     c.shutter_speed = shutter_speed
#     # Let auto exposure camera do its thing
#     time.sleep(2)
#     c.exposure_mode = 'off'
#     return c.shutter_speed, c.iso


# def AutoWB(c: PiCamera, newgain=None):
#     if newgain == None:
#         c.awb_mode = 'auto'
#         # Let AWB do its thing
#         time.sleep(2)
#         g = c.awb_gains
#         # Now lock the white balance
#         c.awb_mode = 'off'
#         c.awb_gains = g
#     else:
#         c.awb_mode = 'off'
#         c.awb_gains = newgain

#     print("awb_mode", c.awb_mode, "awb_gains", c.awb_gains)
#     return c.awb_gains

# def SetExposure(c: PiCamera, shutter_speed: int = 1000, iso: int = 100):
#     print("BEFORE: analog_gain", c.analog_gain, "digital_gain", c.digital_gain)
#     1# Fix camera gain and white balance
#     if c.iso != iso:
#         c.iso = iso
#         # Let camera settle
#         time.sleep(2)

#     #c.exposure_mode = 'auto'
#     #time.sleep(0.5)
#     c.shutter_speed = shutter_speed
#     c.exposure_mode = 'off'
#     print("AFTER: iso", c.iso, "exposure_mode", c.exposure_mode, "exposure_speed", c.exposure_speed,
#           "shutter_speed", c.shutter_speed)


# def configureHighResCamera():
#     global camera

#     if camera == None:
#         print('Configuring high res camera settings')
#         # Close the preview camera object
#         # if camera!=None and camera.closed==False:
#         #    camera.close()

#         # 3840,2496 = 9,584,640pixels
#         # 4064,3040 = 12,330,240pixels
#         # 3840x2896 = 11,120,640pixels
#         # 1920,1440
#         # 2880x2166 = 6,266,880pixels
#         # 3008x2256 = 6,786,048
#         # 3104x2336 = 7,250,944
#         res = (3104, 2336)
#         #Mode 2
#         res = (2048, 1520)
#         camera = PiCamera(resolution=res, framerate=30)
#         #Mode0 is default, Mode 2 uses binning
#         #Mode 2 uses 2028x1520 (half resolution and 2x2binning (softer image))
#         camera.sensor_mode=2
#         camera.exposure_mode = 'auto'
#         camera.awb_mode = 'auto'
#         camera.meter_mode = 'backlit'
#         #Down the contrast a little (default 0)
#         camera.contrast = -10

#     return camera.resolution[0], camera.resolution[1]


# def configureLowResCamera():
#     global camera

#     if camera != None and camera.closed == False:
#         camera.close()

#     res = (640, 480)
#     camera = PiCamera(resolution=res, framerate=30)
#     #Mode0 is default, Mode 2 uses binning
#     camera.sensor_mode=0

#     camera.exposure_mode = 'auto'
#     camera.awb_mode = 'auto'
#     camera.meter_mode = 'backlit'

#     #Down the contrast a little (default 0)
#     camera.contrast = -10

#     return camera.resolution[0], camera.resolution[1]

def confirgureLowResCamera():
    global camera

    if camera != None and camera.closed == False:
        camera.close()

    res = (640, 480)

    picam2 = Picamera2()

    camera_config = picam2.create_still_configuration()

    # camera_config = picam2.create_preview_configuration(main={"size": res})
    
    picam2.configure(camera_config)

    picam2.start_preview(Preview.QTGL)

    picam2.start()

    time.sleep(2)

    picam2.capture_file("test.jpg")