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

HORIZONTAL = 2047
VERTICAL = 0 
    
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
    while (KIPR.get_motor_position_counter(LIFT_MOTOR) < 2232):
		KIPR.motor(LIFT_MOTOR, 50)
    KIPR.motor(LIFT_MOTOR, 0)

def raise_claw_higher():
    while (KIPR.get_motor_position_counter(LIFT_MOTOR) < 3400):
		KIPR.motor(LIFT_MOTOR, 50)
    KIPR.motor(LIFT_MOTOR, 0)
            
def lower_claw():
    while (KIPR.get_digital_value(0) == 0):
		KIPR.motor(LIFT_MOTOR, -50)
    KIPR.motor(LIFT_MOTOR, 0)
    clear_counter(LIFT_MOTOR)
            
def claw(end_pos):
     KIPR.set_servo_position(CLAW_SERVO, end_pos)
     KIPR.msleep(500)
         
def claw_twist(end_pos):
     KIPR.set_servo_position(TURNING_SERVO, end_pos)
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
    print("Make sure to lower claw")
    KIPR.enable_servos()
    claw_twist(HORIZONTAL)
    lower_claw()
    #open claw
    claw(CLAW_OPEN)
    wfl()
    #turn
    clear_counter(R_MOTOR)
    while (KIPR.get_motor_position_counter(R_MOTOR) > -693):
		move(0, -100)
    stop(100)
    #raise claw
    raise_claw()
    KIPR.msleep(100)
    #close claw
    claw(CUBE_GRAB)
    KIPR.msleep(2000)
    #turn
    while (KIPR.get_motor_position_counter(R_MOTOR) < 880):
		move(0, 100)
    stop(100)
    #open claw
    lower_claw()
    claw(CLAW_OPEN)
    #raise claw
    raise_claw_higher()        
    #turn back to position 0
    while (KIPR.get_motor_position_counter(R_MOTOR) > 0):
		move(0, -100)
    stop(100)  
    #pipe align
    move(100, 100, 1800)
    stop(500)
    #go back
    move(-100, -100, 6000)
    #back up
    move(50, 50, 500)
    move(0, 50, 1170)
    move(50, 0, 3650)
    stop(100)
    #grab cube
    lower_claw()
    KIPR.msleep(500)
    claw(CUBE_GRAB)
    raise_claw_higher()
    #turn then drive forward
    move(-50, -50, 800)
    move(0, 50, 2600)
    move(50, 50, 2000)
    move(0, 50, 2000)
    stop(100)
    #drop cube
    lower_claw()
    claw(CLAW_OPEN)
    
    

    
    

    

# --------------------------------------------------------------
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    #setup()
    main()
