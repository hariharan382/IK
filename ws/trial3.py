import pygame
import numpy as np

joy=[]

def handleJoy(e):
    if e.type == pygame.JOYAXISMOTION:
        axis="unknown"
        if (e.dict['axis'] == 0):
            axis="X"
        if (e.dict['axis'] == 1):
            axis="Y"
        if (e.dict['axis'] == 2):
            axis = "throttle"

        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            output(str, e.dict['joy'])

        if e.type == pygame.JOYBUTTONDOWN:
            str = "Button: %d" % (e.dict['button'])
            output(str, e.dict['joy'])
        for i in np.arange(1,12,1):
            if (e.dict['button'] == i):
                print(e)

def output(line, stick):
    print("Joystick: %d; %s" % (stick, line))

def joystickControl():
    while True:
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):
            handleJoyEvent(e)

# main method
def main():
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print("\nPlease connect a joystick and run again.\n")
        quit()
    print("\n%d joystick(s) detected." % pygame.joystick.get_count())
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print("Joystick %d: " % (i) + joy[i].get_name())
    print("Depress Button 8 to quit.\n")

    joystickControl()

if __name__ == "__main__":
    main()