import config as con
try:
	import serial
except:
	con.CONNECT_OUT_FLAG=0
else:
	con.CONNECT_OUT_FLAG=1
import time
import error_handle as eh


def initialize_arducom():
	
	if con.BOARD_INFO!=None:

###########################################################################################################################

		for ddr_index in con.BOARD_OUTPUT:
			if ddr_index[0]!="n.c.":
				con.ddr_DATA=(con.ddr_DATA<<1) | 1
			else:
				con.ddr_DATA=(con.ddr_DATA<<1)
	
###########################################################################################################################
		
		print "Initializing serial port communication with board..."
		
		try:
			con.arduinoSerialData=serial.Serial(con.PORT_NAME,115200,timeout=0.5)
		except:
			eh.display_error(0,0,-5,con.PORT_NAME)
		
		t=time.clock()

###########################################################################################################################

		while (time.clock()-t)<2.0:
			pass

###########################################################################################################################
			
		while (time.clock()-t)<3.0:
			
			if (con.arduinoSerialData.inWaiting()>0):
				con.arduinoSerialData.flush()
				con.arduinoSerialData.readline()
		
			con.arduinoSerialData.write(str(con.ddr_DATA)+",\n")
			
###########################################################################################################################
		
		print "Serial port communication with board established successfully"
		
###########################################################################################################################
		
		for  board_output_index in range(len(con.BOARD_OUTPUT)):
		
			for node_traverse in con.NODE_DATA:
				if con.BOARD_OUTPUT[board_output_index][0]!="n.c.":
					if con.BOARD_OUTPUT[board_output_index][0]==node_traverse[0]:
						con.BOARD_OUTPUT[board_output_index][1]=node_traverse[1]
						break


		for board_input_index in range(len(con.BOARD_INPUT)):
		
			for node_traverse in con.NODE_DATA:
				if con.BOARD_INPUT[board_input_index][0]!="n.c.":
					if con.BOARD_INPUT[board_input_index][0]==node_traverse[0]:
						con.BOARD_INPUT[board_input_index][1]=node_traverse[1]
						break
		
		
		for pin in range(len(con.BOARD_OUTPUT)):
			if con.BOARD_OUTPUT[pin][0]!='n.c.':
				  
				for tb_en in con.tristate_buffer_list:
					if tb_en[0]==con.BOARD_OUTPUT[pin][1]:
						con.BOARD_OUTPUT[pin][2]=tb_en[1:]

###########################################################################################################################

def arduino2python(lock):
	con.arduinoSerialData.flush()
	
	if(con.arduinoSerialData.inWaiting()):
		con.board_input_data=con.arduinoSerialData.readline()
		con.board_input_data='{0:016b}'.format(int(con.board_input_data[:-2]))
	
	for data_index in range(len(con.board_input_data)):	
		if con.BOARD_INPUT[data_index][0]!="n.c.":
			lock.acquire()
			con.NODE_DATA[con.BOARD_INPUT[data_index][1]][2]=int(con.board_input_data[data_index])
			lock.release()
	
###########################################################################################################################
	
def python2arduino(lock):
	
	board_output_data=0
	for data_index in range(16):	
		if con.BOARD_OUTPUT[data_index][0]=="n.c.":
			board_output_data=board_output_data<<1
		elif con.BOARD_OUTPUT[data_index][0]!="n.c.":
			lock.acquire()
			board_output_data=(board_output_data<<1) | con.NODE_DATA[con.BOARD_OUTPUT[data_index][1]][2]
			lock.release()
	
	
	serial_data_out=str(con.DDR_DATA)+","+str(board_output_data)+"\n"
	
	con.arduinoSerialData.write(serial_data_out)

###########################################################################################################################
