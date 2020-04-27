import requests
import time
import datetime as dt
import threading
from presentation_gui import PresentationAPP

WIDTH = 1000
HEIGHT = 800

#Communication Config
PP_ADDRESS = "http://10.0.0.33:8080"
PP_CHANNELS = ["accX", "accY", "accZ", "gyrX", "gyrY", "gyrZ"]

#For receiving values from Phyphox
accX = []
accY = []
accZ = []

gyrX = []
gyrY = []
gyrZ = []



def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    accX = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    accY = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    accZ = data["buffer"][PP_CHANNELS[2]]["buffer"][0]

    gyrX = data["buffer"][PP_CHANNELS[3]]["buffer"][0]
    gyrY = data["buffer"][PP_CHANNELS[4]]["buffer"][0]
    gyrZ = data["buffer"][PP_CHANNELS[5]]["buffer"][0]
    
    return [accX, accY, accZ, gyrX, gyrY, gyrZ]


def getData():
    [naccX, naccY, naccZ, ngyrX, ngyrY, ngyrZ] = getSensorData()
    accX.append(naccX)
    accY.append(naccY)
    accZ.append(naccZ)

    gyrX.append(ngyrX)
    gyrY.append(ngyrY)
    gyrZ.append(ngyrZ)

    return [naccX, naccY, naccZ, ngyrX, ngyrY, ngyrZ]



def data_main(GUI):   
    # EXAMPLE USE OF PRESENTATION APP
    # ON TILT RIGHT -> app.show_slides("FORWARD")
    # ON TILT LEFT -> app.show_slides("BACKWARD")
    # ON CLICK -> app.click()
    # ON MOUSE MOVE -> app.mouse_move(x_offset, y_offset)
    #For initial calibration
    calibratedX = 0
    calibratedY = 0
    
    while True:
        [naccX, naccY, naccZ, ngyrX, ngyrY, ngyrZ] = getData()
        
        #Very basic calibration
        if calibratedX == 0 and calibratedY == 0:
            for i in range(300):
                calibratedX += float(naccX)
                calibratedY += float(naccY)
                time.sleep(.01)

            calibratedX /= 300
            calibratedY /= 300
            print("Calibrated accX: ", calibratedX)
            print("Calibrated accY: ", calibratedY)
            print("Calibrated and ready!")


        # Tilt Check
          # If change in accx spikes positive and gyrz spikes negative tilt right
          # If change in accx spikes negative and gyrz spikes positive tilt left
              #Backwards needs some work with better identification
        if (naccX > (calibratedX + 7) and ngyrZ < -6):
        #if (ngyrZ < -6):
            print("Current accX: ", naccX)
            print("Current ngyrZ: ", ngyrZ)
            print("Going forwards!")
            GUI.show_slides("FORWARD")
            time.sleep(0.6)
        elif (naccX < (calibratedX - 7) and ngyrZ > 6 ):
        #elif (ngyrZ > 6):
            print("Current accX: ", naccX)
            print("Current ngyrZ: ", ngyrZ)
            print("Goimg backwards!")
            GUI.show_slides("BACKWARD")
            time.sleep(0.6)

        # Squeeze
            # Take the ngyrX, ngyrY, ngyrZ measurements and smoosh them together into one variable
            # If this variable reaches a certain threshold, squeeze is detected
        everyGyr = (ngyrX * ngyrY * ngyrZ)

        print("Master Gyroscope value: ", everyGyr)
        print("Accelerometer: ", naccX, ' ', naccY, ' ', naccZ, ' \n',
              "Gyroscope: ", ngyrX, ' ', ngyrY, ' ', ngyrZ)

def gui_main(GUI):
    app.run()
    
    
def main():
    app = PresentationAPP(WIDTH, HEIGHT)
    app.init_images()
    app.show_slides("FORWARD")

    # Start threads
    data_thread = threading.Thread(target=data_main, args=(app,), daemon=True)
    gui_thread = threading.Thread(target=gui_main, args=(app,), daemon=True)

    data_thread.start()
    gui_thread.start()


if __name__ == '__main__':
    main()
    
