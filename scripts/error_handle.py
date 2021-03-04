import config as con
import time
try:
	import serial.tools.list_ports
except:
	con.CONNECT_OUT_FLAG=0
else:
	con.CONNECT_OUT_FLAG=1
def is_numeric(n):
	try:
		int(n)
		return True
	except	ValueError:
		return False

def display_error(LINE,line_index,error_code,error_data):
	
###########################################################################################################################

	ckt_description=["MAINCKT","SUBCKT","MAINCKT_SETUP","CONNECT_OUT_ARDUINO"]
	if error_code>=0:
		line_index+=1
		if LINE[-1]=="\n":
			LINE=LINE[:-1]
	
		print "\n"
		print "Error found at line ",line_index
		print LINE+str("<")

###########################################################################################################################
	
	if error_code==0:
		print "No such command : ",error_data
	elif error_code==1:
		print "PRINT/PRINTF command has no nodes"
	elif error_code==2:
		print "PRINT/PRINTF arguments must be of type integer : ",error_data
	elif error_code==3:
		print "SCAN command has no nodes"
	elif error_code==4:
		print "SCAN arguments must be of type integer : ",error_data
	elif error_code==5:
		print "PLOT command has no nodes"
	elif error_code==6:
		print "PLOT arguments must be of type integer : ",error_data
	elif error_code==7:
		print "CLOCK requires 5 arguments, given :",error_data
	elif error_code==8:
		print "CLOCK arguments must be of type positive integer :",error_data
	elif error_code==9:
		print "FIX_VOLTAGE not allowed outside circuit description"
	elif error_code==10:
		print "FIX_VOLTAGE requires 2 arguments, given : ",error_data
	elif error_code==11:
		print "FIX_VOLTAGE arguments must be of type integer : ",error_data
	elif error_code==12:
		print "TIME_ANALYSIS_SETUP requires at least 2 arguments, given ",error_data
	elif error_code==13:
		print "TIME_ANALYSIS_SETUP arguments must be of type int : ",error_data
	elif error_code==14:
		print "Cannot start MAINCKT description while ",ckt_description[error_data-1]," description is still open"
	elif error_code==15:
		print "MAINCKT description cannot be ended without a starting point"
	elif error_code==16:
		print "ANALYSIS type not mentioned"
	elif error_code==17:
		print "TT_ANALYSIS requires a minimum of 1 and a maximum of 2 arguments, given ",error_data
	elif error_code==18:
		print "SIMULATION_TIME must be of a positive integer : ",error_data
	elif error_code==19:
		print "Invalid ANALYSIS type : ",error_data
	elif error_code==20:
		print "Cannot start SUBCKT description while ",ckt_description[error_data-1]," description is still open"
	elif error_code==21:
		print "SUBCKT defintion requires atleast one node"
	elif error_code==22:
		print "SUBCKT definition arguments must be of type positive int : ",error_data
	elif error_code==23:
		print "SUBCKT description cannot be ended without a starting point"
	elif error_code==24:
		print "Cannot start MAINCKT_SETUP description while ",ckt_description[error_data-1]," description is still open"
	elif error_code==25:
		print "MAINCKT_SETUP definition requires atleast one node"
	elif error_code==26:
		print "MAINCKT_SETUP arguments must be of type int",error_data
	elif error_code==27:
		print "MAINCKT_SETUP description cannot be ended without a starting point"
	elif error_code==28:
		print "Number of voltage values provided do not match the number of nodes at MAINCKT_SETUP definition"
	elif error_code==29:
		print "Data values must be positive integers :",error_data
	elif error_code==30:
		print "Name of SUBCKT to be called not mentioned",error_data
	elif error_code==31:
		print "GATE takes 2 arguments, given :",error_data
	elif error_code==32:
		print "Expression not recognised :",error_data
	elif error_code==33:
		print "SUBCKT \'",error_data,"\' not found"
	elif error_code==34:
		print "Node number mismatch between called and defined SUBCKT"
	elif error_code==35:
		print "SUBCKT name not mentioned"
	elif error_code==36:
		print "GATE arguments must be of type positive integer :",error_data
	elif error_code==37:
		print "GATE takes 3 arguments, given :",error_data
	elif error_code==38:
		print "GATE arguments must be of type positive integer :",error_data
	elif error_code==39:
		print "End of ",ckt_description[error_data-1]," not found"
	elif error_code==40:
		print "CLOCK not allowed outside MAINCKT description"
	elif error_code==41:
		print "Expression not allowed outside circuit description"
	elif error_code==42:
		print "SUBCKT call arguments must be of type positive integer :",error_data
	elif error_code==43:
		print "Node not defined : ",error_data
	elif error_code==44:
		print "CLOCK input cannot be defined more than once"
	elif error_code==45:
		print "Package matplotlib required to use !PLOT command"
	elif error_code==46:
		print "MAINCKT setup file '",error_data,"' not found"
	elif error_code==47:
		print "Inside file '",error_data[0],"' at line ",(error_data[1]+1),"\nNumber of voltage values provided do not match the number of nodes at MAINCKT_SETUP definition"
	elif error_code==48:
		print "Inside file '",error_data[0],"' at line ",(error_data[1]+1),"\nData values must be of type integer : ",error_data[2]
	elif error_code==49:
		print "Subcircuit name not mentioned at subcircuit definition"
	elif error_code==50:
		print "Board '",error_data,"' not recognised"
	elif error_code==51:
		print "Cannot start CONNECT_OUT_ARDUINO description while ",ckt_description[error_data-1]," description is still open"
	elif error_code==52:
		print "CONNECT_OUT_ARDUINO description cannot be ended without a starting point"
	elif error_code==53:
		print "Invalid pin assignment for CONNECT_OUT_ARDUINO description, write the node number followed by the arduino pin name"
	elif error_code==54:
		print "Unsupported pin type for board ",error_data[1],":",error_data[0]
	elif error_code==55:
		print "Package pyserial required to use !PLOT command"
	elif error_code==56:
		print "Invalid assignment of table input/output data file name :",error_data
	elif error_code==57:
		print "Inside file '",error_data[0],"' at line ",(error_data[1]+1),"\nNumber of voltage values provided do not match the number of input nodes provided as TT_ANALYSIS argument"
	elif error_code==58:
		print "Inside file '",error_data[0],"' at line ",(error_data[1]+1),"\nNode voltages must be of type integer : ",error_data[2]
	elif error_code==59:
		print "!CONNECT_OUT_ARDUINO requires 2 arguments, the board name and the port name, given :",error_data
	elif error_code==60:
		print "!WRITE_TO_FILE takes 1 argument as the output file name, given",error_data
	elif error_code==61:
		print "Input file",error_data,"for TT_ANALYSIS not found"
	elif error_code==62:
		print "Input nodes for TT_ANALYSIS must be of type int : ",error_data
	elif error_code==63:
		print "Node voltages can be 0 or 1 only :",error_data
	elif error_code==64:
		print "Inside file '",error_data[0],"' at line ",(error_data[1]+1),"\nNode voltages can be 0 or 1 only :",error_data[2]

###########################################################################################################################

	elif error_code==-1:
		print "Voltage input must be 0 or 1 : ",error_data
	elif error_code==-2:
		print "Voltage input must be of type integer"
	elif error_code==-3:
		print "Circuit file '",error_data,"' not found inside current directory"
	elif error_code==-4:
		print "Invalid file name entered"
	elif error_code==-5:
		print "Failed to establish serial communication with arduino board"
		print "Port '",error_data,"' not found"
		print "Following are the list of available COM ports"
		print [comport.device for comport in serial.tools.list_ports.comports()]
	elif error_code==-6:
		print "The program has stopped working unexpectedly"
###########################################################################################################################
	
	_=raw_input()
	exit()
	
###########################################################################################################################
