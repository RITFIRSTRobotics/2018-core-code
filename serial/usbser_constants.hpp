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
#define INIT_MESSAGE "i0:%c" // initialization string (replace %c with color (r or b))

#define CALIBRATE_MESSAGE "cl:%b" // calibrate goal %b

#define CONTROLLER_DATA "md:%b:%b:%b" // movement data of the two sticks (%b is an unsigned byte) 
                                      //and a number representative of all the buttons being pressed

#define SCORE_DATA "sd:%b" // data sent when a goal has been made (send just the goal number, FMS is responsbile for the point value)

#endif
