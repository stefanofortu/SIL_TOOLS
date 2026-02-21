import serial.tools.list_ports
import time
'''
######################################################
# SERIAL PROTOCOL DEFINITION
######################################################
- Type of communication: STRING [HEXADECIMAL CHAR WITH SEPARATORS ':']
Example --> '0:1:1:0'
- Lenght of the messages: VARIABLES
- First Value defines the message type
######################################################
# MESSAGE FROM PYTHON TO ARDUINO

## MESSAGE TYPE '0'
The purpose of this message is to verify that the connection is ok
There are no parameters to be added
- Signature     '0' 
- Example       '0 
Arduino must reply with 'Arduino_COM_OK' value
- Signature     '0:parameter'
- Example       '0:Arduino_COM_OK'

## MESSAGE TYPE '1'
The purpose of this message is to get the Arduino application name
There are no parameters to be added
- Signature     '1' 
- Example       '1 
Arduino must reply with the name of the application. 
Possible values are "PWM", "PERF_CURVE"
- Signature     '1:parameter'
- Example       '1:PWM'
'''
## MESSAGE TYPE '2'
#The purpose of this message is to get the status of the all the arduino output
#- Signature     '2'
#- Example       '2'
#Arduino must reply with '2:' followed by all the parameters id and the parameters value.
#Each parameters must be in HEX format
#- Signature     '2:parameter1_ID:parameter1_value:parameter2_ID:parameter2_value:parameter3_ID:parameter3_value.....'
#- Example       '2:0:F:A:B4"
#--> !!!this makes no sense: perform iteration on single parameters instead!!!!

#### DOCS for application "PWM"
#The parameters returned are the duty cycle of all the output, from 0 to 10 (parameters ID from 1 to 10)
#--> !!!this makes no sense: perform iteration on single parameters instead!!!!
'''
## MESSAGE TYPE '3': READ SINGLE PARAMETER 
The purpose of this message is to READ a SINGLE parameters into the Arduino. All values must be in HEX format.
- Signature     '3:parameter_id' 
- Example       '3:1'
Arduino must reply with '4:' followed by the parameter id and the value read. All values must be in HEX format.
- Signature     '3:parameter_values_set'
- Example       '3:1:0A"


## MESSAGE TYPE '4': SET SINGLE PARAMETER 
The purpose of this message is to SET a SINGLE parameters into the Arduino. All values must be in HEX format.
- Signature     '4:parameter_id:parameter_value' 
- Example       '4:1:OA' 
Arduino must reply with '4:' followed by the parameter id and the actual value set. All values must be in HEX format.
- Signature     '4:parameter_values_set'
- Example       '4:1:0A"


######################################################
##### PARAMETERS LIST 
######################################################
##### APPLICATION 'PWM'

## DUTY CYCLE
Consider a offset "DUTY_CYCLE_PARAMETER_ID_OFFSET" equal to 16 to map parameter_ID and pump_ID(*)
ID[Dec]     ID[Hex]     Value Range [Hex]   Meaning
17          11          0 - 64              Value of the d.c of the 1st PWM output
18          12          0 - 64              Value of the d.c of the 2nd PWM output
19          13          0 - 64              Value of the d.c of the 3rd PWM output
20          14          0 - 64              Value of the d.c of the 4th PWM output
21          15          0 - 64              Value of the d.c of the 5th PWM output
22          16          0 - 64              Value of the d.c of the 6th PWM output
23          17          0 - 64              Value of the d.c of the 7th PWM output
24          18          0 - 64              Value of the d.c of the 8th PWM output
25          19          0 - 64              Value of the d.c of the 9th PWM output
26          1A          0 - 64              Value of the d.c of the 10th PWM output

## PUMP FEEDBACK
Consider a offset "FEEDBACK_PARAMETER_ID_OFFSET" equal to 32 to map parameter ID and pump_ID(*)
ID[Dec]     ID[Hex]     Value Range [Hex]   Meaning
33          21          0 - 64              ---
34          22          0 - 64              Value of the d.c of the 2nd PWM output !!!!WRONG
35          23          0 - 64              Value of the d.c of the 3rd PWM output !!!!WRONG
36          24          0 - 64              Value of the d.c of the 4th PWM output !!!!WRONG
37          25          0 - 64              Value of the d.c of the 5th PWM output !!!!WRONG
38          26          0 - 64              Value of the d.c of the 6th PWM output !!!!WRONG
39          27          0 - 64              Value of the d.c of the 7th PWM output !!!!WRONG
40          28          0 - 64              Value of the d.c of the 8th PWM output !!!!WRONG
41          29          0 - 64              Value of the d.c of the 9th PWM output !!!!WRONG
42          2A          0 - 64              Value of the d.c of the 10th PWM output !!!!WRONG

(*) pump_ID has value from 1 to 10
'''
class Arduino_Communication():
    def __init__(self):
        self.serial_communication = None
        self.selected_serial_port = None
        self.arduino_connected = False

    def is_connected(self):
        if self.serial_communication:
            if self.serial_communication.is_open:
                if self.arduino_connected:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    def start(self, serial_port_name):
        selected_serial_port_name = serial_port_name
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if selected_serial_port_name == port.description:
                self.selected_serial_port = port.device
                #print(self.selected_serial_port, type(self.selected_serial_port))
        if self.selected_serial_port:
            if self.serial_communication:
                if self.serial_communication.is_open:

                    self.serial_communication.close()
            try:
                print(f"Trying to connect to {self.selected_serial_port}...")
                self.serial_communication = serial.Serial(port=self.selected_serial_port, baudrate=9600, timeout=1)
                # wait for Arduino reset - it is mandatory after setting up serial communication
                time.sleep(2)
                # the re-connection from the serial cause the "setup() loop
                # read all the communication replies get from Arduino at start-up
                self.serial_communication.write(("0" + '\n').encode())
                time.sleep(0.1)
                #read all the replies and discard them
                self.read_all_arduino_messages(verbose=False)
                # now do the actual reading
                self.serial_communication.write(("0" + '\n').encode())
                time.sleep(0.1)
                replies = self.read_all_arduino_messages(verbose=False)
                if replies == "Arduino_COM_OK":
                    print("Connected to Arduino")
                    self.arduino_connected = True
                    return 1  # set green
                else:
                    print("Cannot connect")
                    print("Valore ricevuto:", replies)
                    self.arduino_connected = False
                    return 0  # set orange
            except serial.SerialException as e:
                print(f"❌ SerialException: {e}")
                self.arduino_connected = False
                return -1
            except ValueError as e:
                print(f"❌ ValueError: {e}")
                self.arduino_connected = False
                return -1
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                self.arduino_connected = False
                return -1

    def write_message(self, message, verbose=False):
        if self.arduino_connected:
            self.serial_communication.write((message + '\n').encode())
            time.sleep(0.5)
            all_replies = ""
            while self.serial_communication.in_waiting > 0:
                reply = self.serial_communication.readline().decode().strip()
                if verbose:
                    print("Valore ricevuto:", reply)
                all_replies += (reply + " ")
            return all_replies.strip()
        else:
            print("First connect and then send message")

    def write_and_check_message(self, message, expected_reply):
        if self.arduino_connected:
            self.serial_communication.write((message + '\n').encode())
            time.sleep(0.1)
            reply = self.serial_communication.readline().decode().strip()
            if reply == expected_reply:
                #print("Valore ricevuto:", reply)
                return 1
            else:
                print("Valore ricevuto:", reply)
                return -1
        else:
            print("First re-open connection and then send message")

    def read_all_arduino_messages(self, verbose):
        if self.serial_communication:
            if self.serial_communication.is_open:
                all_replies = ""
                while self.serial_communication.in_waiting > 0:
                    reply = self.serial_communication.readline().decode().strip()
                    if verbose:
                        print("Messages received:", reply)
                    all_replies += (reply + " ")
                return all_replies.strip()

    def close(self):
        if self.serial_communication:
            self.serial_communication.close()
            self.arduino_connected = False
            print("Serial connection closed")

    def __del__(self):
        if self.serial_communication:
            self.serial_communication.close()
            self.arduino_connected = False
            print("Serial connection closed")
