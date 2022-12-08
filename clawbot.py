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
LIFT_MOTOR = 2

CLAW_CLOSED = 2047
CLAW_OPEN = 1100 
CUBE_GRAB = 1770

HORIZONTAL = 1950
VERTICAL = 940   
    
#FUNCTIONS------------------------
clear_counter = KIPR.clear_motor_position_counter

def move(l_power, r_power, sleep_time=5):
    KIPR.motor(L_MOTOR, l_power)
    KIPR.motor(R_MOTOR, r_power)
    KIPR.msleep(sleep_time)    
        
def stop(s_time):
    move(0, 0, s_time)             

def go_to_black(l_power=50, r_power=50):
    while KIPR.analog(TOPH_LEFT) < BLACK or KIPR.analog(TOPH_RIGHT) < BLACK:
        move(l_power, r_power)
            
def go_to_white(l_power=50, r_power=50):
    while KIPR.analog(TOPH_LEFT) > BLACK or KIPR.analog(TOPH_RIGHT) > BLACK:
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
            
def raise_claw():
    clear_counter(LIFT_MOTOR)
    while (KIPR.get_motor_position_counter(LIFT_MOTOR) < 2232):
		KIPR.motor(LIFT_MOTOR, 50)
            
def lower_claw():
    clear_counter(LIFT_MOTOR)
    while (KIPR.get_motor_position_counter(LIFT_MOTOR) > -2232):
		KIPR.motor(LIFT_MOTOR, -50)

def claw(end_pos):
     KIPR.set_servo_position(CLAW_SERVO, end_pos)
     KIPR.msleep(500)
         

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

def main():
    print("Waiting for start light")
    wfl()
	
    #open claw
    claw(CLAW_OPEN)
    #turn
    clear_counter(R_MOTOR)
    while (KIPR.get_motor_position_counter(R_MOTOR) > -737):
		move(0, -100)
    stop(100)
    #raise claw
    raise_claw()
    KIPR.msleep(100)
    #close claw
    claw(CUBE_GRAB)
    #turn
    clear_counter(R_MOTOR)
    while (KIPR.get_motor_position_counter(R_MOTOR) < -737):
		move(0, 100)
    stop(100)
    #lower claw
    lower_claw()
    #open claw
    claw(CLAW_OPEN)
    #pipe align
    #move(100, 100, 4000)
            
    

    
    

    

# --------------------------------------------------------------
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    #setup()
    main()
