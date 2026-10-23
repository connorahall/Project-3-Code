#wall_stop.py
from basehat import UltrasonicSensor
from basehat import Button
from buildhat import Motor
import time   #importing ultrasonic sensor stuff, motor stuff and I guess delta time stuff

def main():
    pin = 5 #defines pin of ultra sonic sensor
    port = 22
    print("Initiating BuildHAT and motors")
    print("this may take a while (~10 seconds)") #printing initiation messages
    motorL = Motor('D')
    motorR = Motor('C') #defining motors with their ports

    button = Button(port)
    ultra = UltrasonicSensor(pin) #defining ultrasonic sensor port
    
    pressCount = 0
    currentlyPressed = False

    try:
        while True: #loop that runs repeataly, keeps programing running
            try:
                value = ultra.getDist #Gets distance from ultrasonic sensor
                
                if not currentlyPressed:
                    pressCount += button.value #adds a 1 if the button has been pressed down
                    currentlyPressed = button.value
                    print("Button was pressed")
                else:
                    currentlyPressed = False

                print(f"Sensor: {value} Motor A: {motorL.get_position()}  B: {motorR.get_position()} PressCount: {pressCount} ")
                if pressCount != 0:
                    if(value != None and value < 10): #if the sensor is working and we are closer then  15cm from object infront of robot
                        motorR.start(-30)
                        motorL.start(30) #reverse motors
                        while (value != None and value <= 15): #until we have backed up beyond 15cm
                            value = ultra.getDist #Gets distance from ultrasonic sensor
                            time.sleep(.1)
                            print(f"Sensor: {value} In first loop")
                        print("Exited first loop")
                        motorL.stop() 
                        motorR.stop()
                        encoderStart = motorL.get_position()
                        motorR.start(-30)
                        motorL.start(-30)
                        while ((abs(motorL.get_position() - encoderStart)) < 60):
                            time.sleep(.02)
                            print(f"Encoder Diff: {abs(motorL.get_position() - encoderStart)} In second loop")
                    else:
                        if pressCount >= 2: #if we are not less then 15cm from wall
                            motorR.start(30)
                            motorL.start(-30)#continue moving
                else:
                   motorL.stop() 
                   motorR.stop() #stop moving
                        
                if button.value and pressCount >= 2:
                    pressCount = 0
                    
                time.sleep(.1) #wait time inbetween updating the loop to not fry the Pis brain

            except IOError: #error catching to not crash pi
                print ("\nError occurred while attempting to read values.")
                motorL.stop()
                motorR.stop()
                break

    except KeyboardInterrupt: #detects when control+c is pressed
        print("\nCtrl+C detected. Exiting...")
        motorL.stop() #stops motors and exits loops\
        motorR.stop()

if __name__ == '__main__': #if we are in the main drive
    main() #run the loop as defined in main
    motorL = Motor('D') #do not know why it is nessecary to initialize these after the main loop is entered.
    motorR = Motor('C')
    motorL.stop() #stops themotors
    motorR.stop()