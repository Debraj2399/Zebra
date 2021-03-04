import config as con

def functional_indexing():

###########################################################################################################################

	for output_node_index in range(len(con.OUTPUT_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.OUTPUT_NODE[output_node_index]==node_traverse[0]:
				con.OUTPUT_NODE_INDEX.append(node_traverse[1])
				break
				
###########################################################################################################################

	for  input_node_index in range(len(con.INPUT_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.INPUT_NODE[input_node_index]==node_traverse[0]:
				con.INPUT_NODE_INDEX.append(node_traverse[1])
				break
	
###########################################################################################################################

	for  scan_node_index in range(len(con.SCAN_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.SCAN_NODE[scan_node_index]==node_traverse[0]:
				con.SCAN_NODE_INDEX.append(node_traverse[1])
				break
				
###########################################################################################################################

	for  print_node_index in range(len(con.PRINT_NODE)):
		if con.PRINT_NODE[print_node_index]!='time':
			for node_traverse in con.NODE_DATA:
				if con.PRINT_NODE[print_node_index]==node_traverse[0]:
					con.PRINT_NODE_INDEX.append(node_traverse[1])
					break
		else:
			con.PRINT_NODE_INDEX.append('time')
		
###########################################################################################################################

	for  printf_node_index in range(len(con.PRINTF_NODE)):
		if con.PRINTF_NODE[printf_node_index]!='time':
			for node_traverse in con.NODE_DATA:
				if con.PRINTF_NODE[printf_node_index]==node_traverse[0]:
					con.PRINTF_NODE_INDEX.append(node_traverse[1])
					break
		else:
			con.PRINTF_NODE_INDEX.append('time')

###########################################################################################################################

	for  plot_node_index in range(len(con.PLOT_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.PLOT_NODE[plot_node_index]==node_traverse[0]:
				con.PLOT_NODE_INDEX.append(node_traverse[1])
				break

###########################################################################################################################

	for  mainckt_setup_node_index in range(len(con.MAINCKT_SETUP_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.MAINCKT_SETUP_NODE[mainckt_setup_node_index]==node_traverse[0]:
				con.MAINCKT_SETUP_NODE_INDEX.append(node_traverse[1])
				break

###########################################################################################################################

	for  time_analysis_setup_node_index in range(len(con.TIME_ANALYSIS_SETUP_NODE)):
		
		for node_traverse in con.NODE_DATA:
			if con.TIME_ANALYSIS_SETUP_NODE[time_analysis_setup_node_index]==node_traverse[0]:
				con.TIME_ANALYSIS_SETUP_NODE_INDEX.append(node_traverse[1])
				break

###########################################################################################################################

	for  tristate_buffer_data in con.MAINCKT_DATA:
		if tristate_buffer_data[0]=="TRISTATE_BUFFER":
			con.TRISTATE_BUFFER_OUTPUT.append(tristate_buffer_data[3])
			con.TRISTATE_BUFFER_ENABLE.append(tristate_buffer_data[1])
	
	temp_delete_list=[]
	
	for tristate_output_index in range(len(con.TRISTATE_BUFFER_OUTPUT)):
		for gate_data in con.MAINCKT_DATA:
			if gate_data[0]!="!FIX_VOLTAGE" and gate_data[0]!="TRISTATE_BUFFER":

				if gate_data[-1]==con.TRISTATE_BUFFER_OUTPUT[tristate_output_index]:
					temp_delete_list.append([con.TRISTATE_BUFFER_OUTPUT[tristate_output_index],con.TRISTATE_BUFFER_ENABLE[tristate_output_index]])
	

	for temp_index in range(len(temp_delete_list)):
		con.TRISTATE_BUFFER_OUTPUT.remove(temp_delete_list[temp_index][0])
		con.TRISTATE_BUFFER_ENABLE.remove(temp_delete_list[temp_index][1])
	
	con.tristate_buffer_list=[]
	
	for tristate_output in con.TRISTATE_BUFFER_OUTPUT:
		duplicate_flag=0
		for tb in con.tristate_buffer_list:
			
			if tb[0]==tristate_output:
				duplicate_flag=1
				break
			
		if duplicate_flag==0:
			tristate_element=[]
			tristate_element.append(tristate_output)
			
			for temp_tristate_index in range(len(con.TRISTATE_BUFFER_OUTPUT)):
				if con.TRISTATE_BUFFER_OUTPUT[temp_tristate_index]==tristate_output:
					tristate_element.append(con.TRISTATE_BUFFER_ENABLE[temp_tristate_index])
			
			con.tristate_buffer_list.append(tristate_element)
	
###########################################################################################################################

	if con.CLOCK_DATA!=None:
		for node_traverse in con.NODE_DATA:
			if con.CLOCK_DATA[0]==node_traverse[0]:
				con.CLOCK_DATA[0]=node_traverse[1]
				node_traverse[2]=con.CLOCK_DATA[4]
				break
