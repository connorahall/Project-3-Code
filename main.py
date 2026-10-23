from basehat import UltrasonicSensor
from basehat import Button
from buildhat import Motor
import time



def main():
    print("Hello World!")
    pass

if __name__ == '__main__':
    main() #run the loop as defined in main
    motorL = Motor('D')
    motorR = Motor('C') 
    motorL.stop()
    motorR.stop()