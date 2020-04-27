import requests
import time
import datetime as dt
import threading
from presentation_gui import PresentationAPP
from queue import Queue

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


def data_main(q):   
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
            print("Please stay put for 3 seconds")
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
            print("Going forwards!")
            q.put([0]) # FORWARDS
            time.sleep(0.6)
        elif (naccX < (calibratedX - 7) and ngyrZ > 6 ):
            print("Goimg backwards!")
            q.put([1]) # BACKWARDS
            time.sleep(0.6)

        # Tap Check
            # Checks Gyroscope and accY for giant spike
        elif (ngyrX < 5 and ngyrX > 1 and ngyrZ < 5 and ngyrZ > 0.5):
            print("You've tapped your phone")
            q.put([2]) # TAPS
            time.sleep(0.05)

        # Pointer Check
        else:
            q.put([3, naccX, naccY])

            
        #print("Accelerometer: ", naccX, ' ', naccY, ' ', naccZ, ' \n', "Gyroscope: ", ngyrX, ' ', ngyrY, ' ', ngyrZ)

if __name__ == '__main__':
    # Initialize App
    app = PresentationAPP(WIDTH, HEIGHT)
    app.init_images()
    app.show_slides("FORWARD")

    # Create queue
    q = Queue()

    # Start threads
    data_thread = threading.Thread(target=data_main, args=(q,))
    data_thread.start()
    
    try:
        app.run(q)
    except KeyboardInterrupt:
        print("QUITTING")
        data_thread.join()
    
    q.join()

