import config as con

###########################################################################################################################

def circuit_construct():

	con.MAINCKT_DATA=add_subckt(con.MAINCKT_DATA)

	for gate_index in range(len(con.MAINCKT_DATA)):
		voltage_value_flag=0
			
		for data_index in range(len(con.MAINCKT_DATA[gate_index])):		
			
			if con.MAINCKT_DATA[gate_index][0]=="!FIX_VOLTAGE" and data_index==2:
				con.FIX_VOLTAGE_INDEX.append(gate_index)
				voltage_value_flag=1
				
			if con.is_number(con.MAINCKT_DATA[gate_index][data_index]) and voltage_value_flag==0:
				con.DUPLICATE_FLAG=0
			
				for node_traverse_index in range(con.NODE_COUNT):
					if con.MAINCKT_DATA[gate_index][data_index]==con.NODE_DATA[node_traverse_index][0]:
						con.MAINCKT_DATA[gate_index][data_index]=con.NODE_DATA[node_traverse_index][1]
						con.DUPLICATE_FLAG=1
						break
				
				if con.DUPLICATE_FLAG==0:
					con.NODE_DATA.append([con.MAINCKT_DATA[gate_index][data_index],con.NODE_COUNT,con.DEFAULT_NODE_VOLTAGE])
					con.MAINCKT_DATA[gate_index][data_index]=con.NODE_COUNT
					con.NODE_COUNT=con.NODE_COUNT+1
	
	for fix_vx in con.FIX_VOLTAGE_INDEX:
		con.NODE_DATA[con.MAINCKT_DATA[fix_vx][1]][2]=con.MAINCKT_DATA[fix_vx][2]
		
	
###########################################################################################################################

def	expand_subckt(subckt):
	
	subckt_name=subckt[1]
	predef_subnodes=subckt[2:]
	
	try:
		SUBCKT_FILE=open(con.PREPATH+"\SUBCIRCUITS_USER_DEFINED\\"+subckt_name+".txt","r")
	except IOError:
		if subckt_name[:2]=="IC":
			SUBCKT_FILE=open(con.PREPATH+"\IC74XX\\"+subckt_name+".txt","r")
		else:
			SUBCKT_FILE=open(con.PREPATH+"\SUBCIRCUITS_INBUILT\\"+subckt_name+".txt","r")
	
	SUBCKT_DATA=SUBCKT_FILE.readlines()
	
	PREDEF_SUBNODES=SUBCKT_DATA[0].split()
	
	for node_index in range(len(PREDEF_SUBNODES)):		
		PREDEF_SUBNODES[node_index]=eval(PREDEF_SUBNODES[node_index]) 
	
	SUBCKT_DATA=SUBCKT_DATA[1:]
	
	SUBCKT_TEMP_NODE_DATA=[]
	SUBCKT_TEMP_NODE_COUNT=0
	
	for subgate_index in range(len(SUBCKT_DATA)):
		SUBCKT_DATA[subgate_index]=SUBCKT_DATA[subgate_index].split()
		voltage_value_flag=0
			
		for data_index in range(len(SUBCKT_DATA[subgate_index])):
			
			if SUBCKT_DATA[subgate_index][0]=="!FIX_VOLTAGE" and data_index==2:
				voltage_value_flag=1
				SUBCKT_DATA[subgate_index][2]=eval(SUBCKT_DATA[subgate_index][2])
				
			if con.is_number(SUBCKT_DATA[subgate_index][data_index]) and voltage_value_flag==0:
				SUBCKT_DATA[subgate_index][data_index]=eval(SUBCKT_DATA[subgate_index][data_index])
			
				con.DUPLICATE_FLAG=0
			
				for node_traverse_index in range(SUBCKT_TEMP_NODE_COUNT):
					if SUBCKT_DATA[subgate_index][data_index]==SUBCKT_TEMP_NODE_DATA[node_traverse_index][0]:
						SUBCKT_DATA[subgate_index][data_index]=SUBCKT_TEMP_NODE_DATA[node_traverse_index][2]
						con.DUPLICATE_FLAG=1
						break
			
				if con.DUPLICATE_FLAG==0:
					prenode_flag=0
				
					for prenodes in range(len(PREDEF_SUBNODES)):
						if SUBCKT_DATA[subgate_index][data_index]==PREDEF_SUBNODES[prenodes]:
							subckt_node_value=predef_subnodes[prenodes]
							prenode_flag=1
							break
				
					if prenode_flag==0:
						subckt_node_value=con.subckt_node_count
						con.subckt_node_count=con.subckt_node_count-1
				
					SUBCKT_TEMP_NODE_DATA.append([SUBCKT_DATA[subgate_index][data_index],SUBCKT_TEMP_NODE_COUNT,subckt_node_value])
					SUBCKT_DATA[subgate_index][data_index]=subckt_node_value
					SUBCKT_TEMP_NODE_COUNT=SUBCKT_TEMP_NODE_COUNT+1

	return SUBCKT_DATA

###########################################################################################################################

def add_subckt(MAINCKT_DATA):

	gate_index=0

	while gate_index<len(MAINCKT_DATA):
		
		if MAINCKT_DATA[gate_index][0]=="SUBCKT":
			subckt=expand_subckt(MAINCKT_DATA[gate_index])
			subckt=add_subckt(subckt)
			MAINCKT_DATA.pop(gate_index)
			MAINCKT_DATA[gate_index:gate_index]=subckt
			gate_index=gate_index+len(subckt)-1
		gate_index=gate_index+1
	return MAINCKT_DATA

###########################################################################################################################
