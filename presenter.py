#import tkinter as tk
import requests

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

    while True:
        [naccX, naccY, naccZ, ngyrX, ngyrY, ngyrZ] = getData()
        print("Accelerometer: ", naccX, ' ', naccY, ' ', naccZ, ' \n',
              "Gyroscope: ", ngyrX, ' ', ngyrY, ' ', ngyrZ)


if __name__ == '__main__':
    main()
    
