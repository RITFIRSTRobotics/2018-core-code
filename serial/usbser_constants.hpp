/**
 * serial/usbser_constants.hpp
 *
 * A bunch of constants used for serial transmission between the FMS and the ASC
 */
#ifndef _serial_constants_hpp
#define _serial_constants_hpp

#define BAUD_RATE 115200 // Baud Rate of the connection

#define NEWLINE '\n' // newline character and end-of-line character

/**
 * Transmitted codes
 *
 * These codes are designed to be as short as possible in the name of speed
 */
#define BLINK_MESSAGE "b0:g"

#define INIT_MESSAGE "i0:%c" // initialization string (replace %c with color (r or b))
#define INIT_RESPONSE "i1:good" // tell the FMS that the ASC has been initialzed

#define CALIBRATE_MESSAGE "c0:%1u" // calibrate goal %b
#define CALIBRATE_RESPONSE "c1:good" // tell the FMS that the goal has been calibrated

#define CONTROLLER_DATA "md:%u:%u:%u:%u:%u" // movement data of the two sticks (%u is an unsigned byte) 
                                            //and a number representative of all the buttons being pressed

#define SCORE_DATA "sd:%d" // data sent when a goal has been made (send just the goal number, FMS is responsbile for the point value)

#endif