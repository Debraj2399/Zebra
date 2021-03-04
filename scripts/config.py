import os
import glob
import sys
import error_handle as eh

###########################################################################################################################

def initialize():

###########################################################################################################################

	global CIRCUIT_FILE
	global CODE_FILE
	global CODE_DATA
	global NODE_DATA
	global NODE_COUNT
	global DEFAULT_NODE_VOLTAGE
	global DUPLICATE_FLAG
	global MAXIMUM_SIMULATION_COUNT
	global INPUT_VARIABLES_COUNT
	global INPUT_VARIABLES_VALUE
	global INPUT_VARIABLES
	global OUTPUT_NODE_INDEX
	global subckt_node_count
	global MAINCKT_SETUP_NODE
	global PRINT_NODE
	global PRINTF_NODE
	global PLOT_NODE
	global FIX_VOLTAGE_NODE
	global SCAN_NODE
	global INPUT_NODE
	global OUTPUT_NODE
	global TIME_ANALYSIS_SETUP_NODE
	global MAINCKT_DATA
	global CLOCK_DATA
	global SETUP_DATA
	global screen
	global initial_x
	global initial_y
	global y_div
	global TRUTH_TABLE_OUTPUT_DATA_FILE
	global TRUTH_TABLE_INPUT_DATA_FILE
	global MAINCKT_SETUP_DATA
	global MAINCKT_SETUP_NODE_INDEX
	global FIX_VOLTAGE_INDEX
	global PRINT_NODE_INDEX
	global PRINTF_NODE_INDEX
	global PLOT_NODE_INDEX
	global SCAN_NODE_INDEX
	global INPUT_NODE_INDEX
	global OUTPUT_NODE_INDEX
	global TRISTATE_BUFFER_ENABLE
	global TRISTATE_BUFFER_OUTPUT
	global tristate_buffer_list
	global ANALYSIS
	global TOTAL_SIMULATION_TIME
	global TIME_ANALYSIS_DATA_FILENAME
	global TIME_ANALYSIS_DATA_FILE
	global TIME_ANALYSIS_SETUP_NODE_INDEX
	global TIME_ANALYSIS_SETUP_COUNT
	global TIME_ANALYSIS_DATA_ARRAY
	global PLOT_DATA
	global PLOT_ALLOW_FLAG
	global TURTLES
	global PREPATH
	global BOARD_NAME
	global BOARD_INPUT
	global BOARD_OUTPUT
	global BOARD_INFO
	global PORT_NAME
	global arduinoSerialData
	global CONNECT_OUT_FLAG
	global board_input_data
	global circuit_simulation_flag
	global maincircuit_setup_simulation_flag
	global serial_communication_flag
	global clocking_flag
	global serial_sync_time
	global serial_sync_time0
	global current_time
	global last_time
	global start_time
	global ddr_DATA
	global DDR_DATA
	global connect_out_tb
	global screen_rt
	global turtle_write
	global temp_print_node
	global temp_height
	global CONNECT_OUT_NODE_OUT
	global CONNECT_OUT_NODE_IN
	global TRUTH_TABLE_INPUT_DATA_FILENAME
	global TRUTH_TABLE_OUTPUT_DATA_FILENAME
	global tt_time_flag
	global serial_sync_time1
	global mcktstp_time_flag
	global MAINCKT_PRINT_ARRAY
	global scan_sampling_time
	global MAINCKT_SETUP_FILENAME
	global print_plot_result1_flag
	global print_plot_result2_flag
	global ANALYSIS_DATA
	global ANALYSIS_DATA_FILENAME
	global end_time
	global tt_time_print_flag
	global tt_time_plot_flag
	
###########################################################################################################################

	PREPATH=os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))	
	
	if len(sys.argv)==2:
		CIRCUIT_FILE=sys.argv[1]
	else:
		eh.display_error(0,0,-4,0)
		
	try:
	
		CODE_FILE=open(CIRCUIT_FILE,"r")
	except:
		eh.display_error(0,0,-3,CIRCUIT_FILE)
		
	CODE_DATA=CODE_FILE.readlines()
	
###########################################################################################################################
	
	TURTLES=[]
	ANALYSIS=None
	TRUTH_TABLE_OUTPUT_DATA_FILE=None
	TRUTH_TABLE_INPUT_DATA_FILE=None
	MAINCKT_SETUP_FILENAME=None
	TOTAL_SIMULATION_TIME=None
	TIME_ANALYSIS_DATA_FILE=None
	FIX_VOLTAGE_INDEX=[]
	PRINT_NODE_INDEX=[]
	PRINTF_NODE_INDEX=[]
	PLOT_NODE_INDEX=[]
	SCAN_NODE_INDEX=[]
	INPUT_NODE_INDEX=[]
	OUTPUT_NODE_INDEX=[]
	TIME_ANALYSIS_SETUP_NODE_INDEX=[]
	TRISTATE_BUFFER_OUTPUT=[]
	TRISTATE_BUFFER_ENABLE=[]
	TIME_ANALYSIS_DATA_ARRAY=[]
	PLOT_DATA=[]
	SETUP_DATA=[]
	MAINCKT_SETUP_DATA=None
	INPUT_VARIABLES_VALUE=[]
	connect_out_tb=[]
	tristate_buffer_list=[]
	CLOCK_DATA=None
	TIME_ANALYSIS_SETUP_NODE=[]
	MAINCKT_SETUP_NODE=[]
	MAINCKT_SETUP_NODE_INDEX=[]
	PRINT_NODE=[]
	PRINTF_NODE=[]
	PLOT_NODE=[]
	SCAN_NODE=[]
	INPUT_NODE=[]
	OUTPUT_NODE=[]
	MAINCKT_DATA=[]
	FIX_VOLTAGE_NODE=[]
	NODE_DATA=[]
	NODE_COUNT=0
	DEFAULT_NODE_VOLTAGE=0
	DUPLICATE_FLAG=0
	MAXIMUM_SIMULATION_COUNT=1
	TIME_ANALYSIS_SETUP_COUNT=0
	INPUT_VARIABLES=[]
	BOARD_INPUT=[]
	BOARD_OUTPUT=[]
	BOARD_INFO=None
	arduinoSerialData=None
	board_input_data="00000000"
	circuit_simulation_flag=True
	maincircuit_setup_simulation_flag=True
	serial_communication_flag=True
	clocking_flag=True
	serial_sync_time=0.03
	ddr_DATA=0
	DDR_DATA=0
	subckt_node_count=-1
	CONNECT_OUT_NODE_OUT=[]
	CONNECT_OUT_NODE_IN=[]
	TRUTH_TABLE_INPUT_DATA_FILENAME=None
	TRUTH_TABLE_OUTPUT_DATA_FILENAME=None
	TIME_ANALYSIS_DATA_FILENAME=None
	tt_time_flag=0
	mcktstp_time_flag=0
	MAINCKT_PRINT_ARRAY=[]
	scan_sampling_time=0.01
	print_plot_result1_flag=True
	print_plot_result2_flag=True
	ANALYSIS_DATA=None
	ANALYSIS_DATA_FILENAME=None
	end_time=0
	tt_time_print_flag=True
	tt_time_plot_flag=True
	
###########################################################################################################################
	
	files=glob.glob(PREPATH+"/SUBCIRCUITS_USER_DEFINED/*")
	for f in files:
		os.remove(f)
	
###########################################################################################################################

def is_number(n):
	try:
		int(n)
		return True
	except	ValueError:
		return False

###########################################################################################################################
