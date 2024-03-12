import os
import math

def calculateAngleForSpoolTakeUp(inner_diameter_spool: float, frame_height: float, film_thickness: float, frames_on_spool: int, new_frames_to_spool: int) -> float:
    '''Calculate the angle to wind the take up spool forward based on
    known number of frames already on the spool and the amount of frames we want to add.
     May return more than 1 full revolution of the wheel (for example 650 degrees)'''
    r = inner_diameter_spool/2
    existing_tape_length = frame_height*frames_on_spool
    spool_radius = math.sqrt(existing_tape_length *
                             film_thickness / math.pi + r**2)
    circumfrence = 2*math.pi * spool_radius
    arc_length = new_frames_to_spool * frame_height
    angle = arc_length/circumfrence*360
    
    return angle

def pointInRect(point, rect):
    if point == None:
        return False
    if rect == None:
        return False

    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])


def OutputFolder(exposures: list) -> str:
    # Create folders for the different EV exposure levels
    for e in exposures:
        path = os.path.join(os.getcwd(), "Capture{0}".format(e))
        if not os.path.exists(path):
            os.makedirs(path)

    # Image Output path - create if needed
    path = os.path.join(os.getcwd(), "Capture")

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def determineStartingFrameNumber(path: str, ext: str) -> int:
    existing_files = sorted(glob.glob(os.path.join(
        path, "frame_????????."+ext)), reverse=True)

    if len(existing_files) > 0:
        return 1+int(os.path.basename(existing_files[0]).split('.')[0][6:])

    return 0

def ServiceImageWriteQueue(q):

    path = OutputFolder([])

    while True:
        data=q.get(block=True, timeout=None)
        
        filename = os.path.join(path+"{0}".format(data["exposure"]), "frame_{:08d}.png".format(data["number"]))
        # Save frame to disk.
        # PNG output, with NO compression - which is quicker (less CPU time) on Rasp PI
        # at expense of disk I/O
        # PNG is always lossless
        #start_time = time.perf_counter()
        #if cv.imwrite(filename, data["image"]) == False:
        if cv.imwrite(filename, data["image"], [cv.IMWRITE_PNG_COMPRESSION, 2])==False:
            raise IOError("Failed to save image")
        #print("Save image took {0:.2f} seconds".format(time.perf_counter() - start_time))
        q.task_done()
