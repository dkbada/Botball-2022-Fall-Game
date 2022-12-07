#!/usr/bin/python
from __future__ import print_function
import os, sys
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

#CONSTANTS-----------------------
R_MOTOR = 1
L_MOTOR = 0   

TOPH_RIGHT = 2
TOPH_LEFT = 1
TOPH_BRIGHT = 4
TOPH_BLEFT = 3
LS = 0
    
BLACK = 1500
BACK_BLACK = 3700  

TURNING_SERVO = 1    
CLAW_SERVO = 0

CLAW_CLOSED = 2047
CLAW_OPEN = 1060    

HORIZONTAL = 1950
VERTICAL = 940   
    
#FUNCTIONS------------------------
def move(l_power, r_power, sleep_time=5):
    KIPR.motor(L_MOTOR, l_power)
    KIPR.motor(R_MOTOR, r_power)
    KIPR.msleep(sleep_time)    
        
def stop(s_time):
    move(0, 0, s_time)             

def go_to_black(l_power=50, r_power=50):
    while(KIPR.analog(TOPH_LEFT) < BLACK or KIPR.analog(TOPH_RIGHT) < BLACK):
        move(l_power, r_power)
            
def go_to_white(l_power=50, r_power=50):
    while(KIPR.analog(TOPH_LEFT) > BLACK or KIPR.analog(TOPH_RIGHT) > BLACK):
        move(l_power, r_power)   
            
def line_follow(time, sensor=TOPH_LEFT):
    end_time = KIPR.seconds() + time
    while KIPR.seconds() < end_time:
        if KIPR.analog(sensor) > BLACK:
            if sensor == TOPH_LEFT:
                move(39, 52)
            else:
                move(52, 39)
        else:
            if sensor == TOPH_LEFT:
                move(52, 39)
            else:
                move(39, 52)

def hold_on():
    KIPR.clear_motor_position_counter(3)
    while KIPR.get_motor_position_counter(3) > -17:        
        KIPR.motor(ARM_MOTOR, -10)
    KIPR.off(ARM_MOTOR)

def servo_control(servo_name, end_pos, rate=1):
    pos = KIPR.get_servo_position(servo_name)
    print(servo_name, pos, end_pos)
    if pos > end_pos:
        for i in range(pos, end_pos, -rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)
    else:
        for i in range(pos, end_pos, rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)            
            
#back line follow            
def blf(time, power): 
    end_time = KIPR.seconds() + time
    while KIPR.seconds() < end_time:
        if KIPR.analog(TOPH_BRIGHT) < BACK_BLACK and KIPR.analog(TOPH_BLEFT) < BACK_BLACK:
            move(-power, -power)
        elif KIPR.analog(TOPH_BRIGHT) < BACK_BLACK and KIPR.analog(TOPH_BLEFT) > BACK_BLACK:
            move(int(-power * 0.67), -power)
        elif KIPR.analog(TOPH_BRIGHT) > BACK_BLACK and KIPR.analog(TOPH_BLEFT) < BACK_BLACK:
            move(-power, int(-power * 0.67))      
                
#wait for light                
def wfl():
    START = KIPR.analog(LS) # Get ambient light
    while KIPR.analog(LS) > START/2:
       stop(200)

def claw():
    servo_control(CLAW_SERVO)


def main():
    print("Waiting for start light")
    #arm_setup(-15, 200)
    #KIPR.off(3)        
    wfl()  
    #move forward
    move(100, 100, 4000)
    move(100, 80, 1000)

    

# --------------------------------------------------------------
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    setup()
    main()
