from socket import timeout
import numpy as np
import serial
from datetime import datetime, timedelta

def MarlinWaitForReply(MarlinSerialPort: serial.Serial, echoToPrint=True) -> bool:
    tstart = datetime.now()

    while True:
        # Wait until there is data waiting in the serial buffer
        if MarlinSerialPort.in_waiting > 0:
            # Read data out of the buffer until a CR/NL is found
            serialString = MarlinSerialPort.readline()

            if echoToPrint:
                if serialString.startswith(b"echo:"):
                    # Print the contents of the serial data
                    print("Marlin R:", serialString.decode("Ascii"))

            if serialString == b"ok\n":
                return True

            # Reset delay since last reception
            tstart = datetime.now()

        else:
            # Abort after X seconds of not receiving anything
            duration = datetime.now()-tstart
            if duration.total_seconds() > 3:
                return False


def SendMarlinCmd(MarlinSerialPort: serial.Serial, cmd: str) -> bool:
    print("Sending GCODE", cmd)

    if MarlinSerialPort.isOpen() == False:
        raise Exception("Port closed")

    # Flush input buffer
    MarlinSerialPort.flushInput()
    MarlinSerialPort.flushOutput()
    MarlinSerialPort.read_all()

    MarlinSerialPort.write(cmd.encode('utf-8'))
    MarlinSerialPort.write(b'\n')
    if MarlinWaitForReply(MarlinSerialPort) == False:
        raise Exception("Bad GCODE command or not a valid reply from Marlin")

    return True


def SendMultipleMarlinCmd(MarlinSerialPort: serial.Serial, cmds: list) -> bool:
    for cmd in cmds:
        SendMarlinCmd(MarlinSerialPort, cmd)
    return True


def MoveFilm(marlin: serial.Serial, y: float, feed_rate: int):
    SendMarlinCmd(marlin, "G0 Y{0:.4f} F{1}".format(y, feed_rate))
    # Dwell
    #SendMarlinCmd(marlin,"G4 P100")
    # Wait for move complete
    SendMarlinCmd(marlin, "M400")


def MoveReel(marlin: serial.Serial, z: float, feed_rate: int, wait_for_completion=True):
    # Used to rewind the reel/take up slack reel onto spool
    SendMarlinCmd(marlin, "G0 Z{0:.4f} F{1}".format(z, feed_rate))
    if wait_for_completion:
        # Wait for move complete
        SendMarlinCmd(marlin, "M400")


def SetMarlinLight(marlin: serial.Serial, level: int = 255):
    # print("Light",level)
    if level > 0:
        # M106 Light (fan) On @ PWM level S
        SendMarlinCmd(marlin, "M106 S{0}".format(level))
    else:
        # M107 Light Off
        SendMarlinCmd(marlin, "M107")


def ConnectToMarlin():
    #ports = list(port_list.comports())
    # for p in ports:
    #    print (p)

    # Connect to MARLIN
    marlin = serial.Serial(
        port="/dev/ttyUSB0", baudrate=250000, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE
    )

    # After initial connection Marlin sends loads of information which we ignore...
    MarlinWaitForReply(marlin, True)

    # Send setup commands...
    # M502 Hardcoded Default Settings Loaded
    # G21 - Millimeter Units
    # M211 - Software Endstops (disable)
    # G90 - Absolute Positioning
    # M106 - Fan On (LED LIGHT)
    # G92 - Set Position
    # M201 - Set Print Max Acceleration (off)
    # M18 - Disable steppers (after 15 seconds)
    SendMultipleMarlinCmd(
        marlin, ["M502", "G21", "M211 S0", "G90", "G92 X0 Y0 Z0", "M201 Y0", "M18 S15", "M203 X1000.00 Y1000.00 Z5000.00"])

    SetMarlinLight(marlin, 255)

    # M92 - Set Axis Steps-per-unit
    # Just a fake number to keep things uniform, 10 steps
    # 8.888 steps for reel motor, 1 unit is 1 degree = 360 degrees per revolution
    SendMarlinCmd(marlin, "M92 Y10 Z8.888888")

    # Wait for movement to complete
    SendMarlinCmd(marlin, "M400")
    return marlin


def DisconnectFromMarlin(serial_port: serial.Serial):
    # M107 Light Off
    # M84 Steppers Off
    SetMarlinLight(serial_port, 0)
    SendMultipleMarlinCmd(serial_port, ["M84"])
    serial_port.close()