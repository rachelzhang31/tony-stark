#import tkinter as tk
import requests
from presentation_gui import PresentationAPP

WIDTH = 1000
HEIGHT = 800

#Communication Config
PP_ADDRESS = "http://10.0.0.33:8080"
PP_CHANNELS = ["accX", "accY", "accZ", "gyrX", "gyrY", "gyrZ"]

accX = []
accY = []
accZ = []

gyrX = []
gyrY = []
gyrZ = []


#window = tk.Tk()


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

def main():
    
    app = PresentationAPP(WIDTH, HEIGHT)
    app.show_slides("FORWARD")
    app.run()

    while True:
        [naccX, naccY, naccZ, ngyrX, ngyrY, ngyrZ] = getData()
        print("Accelerometer: ", naccX, ' ', naccY, ' ', naccZ, ' \n',
              "Gyroscope: ", ngyrX, ' ', ngyrY, ' ', ngyrZ)
        
        # EXAMPLE USE OF PRESENTATION APP
        # ON TILT RIGHT -> app.show_slides("FORWARD")
        # ON TILT LEFT -> app.show_slides("BACKWARD")
        # ON CLICK -> app.click()
        # ON MOUSE MOVE -> app.mouse_move(x_offset, y_offset)

if __name__ == '__main__':
    main()
    
