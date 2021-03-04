import error_handle as eh
import config as con

def scan_code(SCRIPT):
	
###########################################################################################################################

	circuit_flag=0
	clock_count=0
	nodes_list=[]
	subckt_nodes_list=[]
	arduino_pin_list=[]
	length=len(SCRIPT)

###########################################################################################################################

	for line_index in range(length):
		LINE=SCRIPT[line_index]
		
		if LINE[0]=="*":
			continue
			
		line=LINE.split()
		
		if line==[]:
			continue
			
		for word_index in range(len(line)):
			if eh.is_numeric(line[word_index]):
				line[word_index]=eval(line[word_index])

###########################################################################################################################
		if eh.is_numeric(line[0]):
			eh.display_error(LINE,line_index,32,LINE)
			continue
		elif line[0][0]=="!":
			
###########################################################################################################################

			if line[0]=="!PRINT":
				arg=line[1:]
				
				if len(arg)==0:
					eh.display_error(LINE,line_index,1,0)
				
				for word in arg:
					if type(word)!=int and word!='time':
						eh.display_error(LINE,line_index,2,str(word))
		
					if not(word in nodes_list) and word!='time':
						eh.display_error(LINE,line_index,43,str(word))
						
				con.PRINT_NODE=line[1:]
				
				continue

###########################################################################################################################

			elif line[0]=="!PRINTF":
				arg=line[1:]
				
				if len(arg)==0:
					eh.display_error(LINE,line_index,1,0)
				
				for word in arg:
					if type(word)!=int and word!='time':
						eh.display_error(LINE,line_index,2,str(word))
		
					if not(word in nodes_list) and word!='time':
						eh.display_error(LINE,line_index,43,str(word))
						
				con.PRINTF_NODE=line[1:]
				
				continue

###########################################################################################################################
			
			elif line[0]=="!SCAN":
				arg=line[1:]
				
				if len(arg)==0:
					eh.display_error(LINE,line_index,3,0)
				
				for word in arg:
					if type(word)!=int:
						eh.display_error(LINE,line_index,4,str(word))
					
					if not(word in nodes_list):
						eh.display_error(LINE,line_index,43,str(word))
						
				con.SCAN_NODE=line[1:]
				continue

###########################################################################################################################
			
			elif line[0]=="!PLOT":
				
				if con.PLOT_ALLOW_FLAG==0:
					eh.display_error(LINE,line_index,45,0)
				
				arg=line[1:]
				
				if len(arg)==0:
					eh.display_error(LINE,line_index,5,0)
				
				for word in arg:
					if type(word)!=int:
						eh.display_error(LINE,line_index,6,str(word))
					
					if not(word in nodes_list):
						eh.display_error(LINE,line_index,43,str(word))
					
				con.PLOT_NODE=line[1:]
				
				continue
			
###########################################################################################################################

			elif line[0]=="!CLOCK":
				clock_count+=1
				arg=line[1:]
				
				if circuit_flag!=1:
					eh.display_error(LINE,line_index,40,0)
				
				if clock_count>1:
					eh.display_error(LINE,line_index,44,0)
				
				if len(arg)!=5:
					eh.display_error(LINE,line_index,7,len(arg))
					
				if not(line[1] in nodes_list):
					eh.display_error(LINE,line_index,43,str(line[1]))
				
				for word in arg:
					if type(word)!=int:
						eh.display_error(LINE,line_index,8,str(word))
					if word < 0:
						eh.display_error(LINE,line_index,8,str(word))
						
				con.CLOCK_DATA=[line[1],(line[2]/1000.0),(line[3]/1000.0),(line[4]/1000.0),line[5],0]
			
				continue

###########################################################################################################################
			
			elif line[0]=="!FIX_VOLTAGE":
				arg=line[1:]

				if circuit_flag!=1 and circuit_flag!=2:
					eh.display_error(LINE,line_index,9,0)
				
				if len(arg)!=2:
					eh.display_error(LINE,line_index,10,len(arg))
				
				if circuit_flag==1:
					if not(line[1] in nodes_list):
						eh.display_error(LINE,line_index,43,line[1])
				elif circuit_flag==2:
					if not(line[1] in subckt_nodes_list):
						eh.display_error(LINE,line_index,43,line[1])
						
				for word in arg:
					if type(word)!=int:
						eh.display_error(LINE,line_index,11,str(word))
				
				if arg[1]!=0 and arg[1]!=1:
					eh.display_error(LINE,line_index,63,str(arg[1]))
				
				if circuit_flag==1 or circuit_flag==0:
					con.MAINCKT_DATA.append(line)
				
				continue

###########################################################################################################################
			
			elif line[0]=="!SET_SCAN_SAMPLING_TIME":
				
				con.scan_sampling_time=(line[1]/1000.0)

				continue

###########################################################################################################################
			
			elif line[0]=="!MAINCKT":
				if circuit_flag!=0:
					eh.display_error(LINE,line_index,14,circuit_flag)
				circuit_flag=1
				continue

###########################################################################################################################
				
			elif line[0]=="!END_MAINCKT":
				if circuit_flag!=1:
					eh.display_error(LINE,line_index,15,0)
				
				circuit_flag=0
				
				if len(line)<2:
					eh.display_error(LINE,line_index,16,0)
				else:
					con.ANALYSIS=line[1]

###########################################################################################################################

					if	con.ANALYSIS=="OT_ANALYSIS":
						continue

###########################################################################################################################
					
					elif	con.ANALYSIS=="RT_ANALYSIS":
						continue

###########################################################################################################################
					
					elif	con.ANALYSIS=="TT_ANALYSIS":
					
						if len(line[2:])>2 or len(line[2:])<1:
							eh.display_error(LINE,line_index,17,len(line[2:]))
							
						con.INPUT_NODE=str(line[2]).split(",")
						con.INPUT_VARIABLES_COUNT=len(con.INPUT_NODE)
						
						for inp_index in range(len(con.INPUT_NODE)):
							
							if not(eh.is_numeric(con.INPUT_NODE[inp_index])):
								eh.display_error(LINE,line_index,62,con.INPUT_NODE[inp_index])
							
							con.INPUT_NODE[inp_index]=eval(con.INPUT_NODE[inp_index])
							
							if not(con.INPUT_NODE[inp_index] in nodes_list):
								eh.display_error(LINE,line_index,43,str(con.INPUT_NODE[inp_index]))
						
						
						if	len(line)>3:

							if line[3][-5:]==":time":
								con.TRUTH_TABLE_INPUT_DATA_FILENAME=str(line[3][:-5])
								con.tt_time_flag=1
							else:
								con.TRUTH_TABLE_INPUT_DATA_FILENAME=str(line[3])
							
							try:
								con.TRUTH_TABLE_INPUT_DATA_FILE=open(str(con.TRUTH_TABLE_INPUT_DATA_FILENAME),"r")
							except IOError:
								eh.display_error(LINE,line_index,61,con.TRUTH_TABLE_INPUT_DATA_FILENAME)
								
							
							if con.TRUTH_TABLE_INPUT_DATA_FILE!=None:
								con.TRUTH_TABLE_INPUT_DATA=con.TRUTH_TABLE_INPUT_DATA_FILE.readlines()
								
								for input_table_data_index in range(len(con.TRUTH_TABLE_INPUT_DATA)):
							
									con.TRUTH_TABLE_INPUT_DATA[input_table_data_index]=con.TRUTH_TABLE_INPUT_DATA[input_table_data_index].split()

									for data_node_index in range(len(con.TRUTH_TABLE_INPUT_DATA[input_table_data_index])):
										
										if not(eh.is_numeric(con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index])):
											eh.display_error(LINE,line_index,58,(con.TRUTH_TABLE_INPUT_DATA_FILENAME,data_node_index,con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index]))
										
										con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index]=eval(con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index])
										
										if data_node_index!=0 and con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index]!=0 and con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index]!=1:
											eh.display_error(LINE,line_index,64,(con.TRUTH_TABLE_INPUT_DATA_FILENAME,data_node_index,con.TRUTH_TABLE_INPUT_DATA[input_table_data_index][data_node_index]))
										
									if len(con.TRUTH_TABLE_INPUT_DATA[input_table_data_index])!=(len(con.INPUT_NODE)+(con.tt_time_flag)):
										eh.display_error(LINE,line_index,57,(con.TRUTH_TABLE_INPUT_DATA_FILENAME,input_table_data_index))
										
									con.INPUT_VARIABLES_VALUE.append(con.TRUTH_TABLE_INPUT_DATA[input_table_data_index])
								
						continue

###########################################################################################################################
					
					elif con.ANALYSIS=="TIME_ANALYSIS":
						
						if len(line)>2:
							if type(line[2])!=int:
								eh.display_error(LINE,line_index,18,line[2])
							if line[2] < 0:
								eh.display_error(LINE,line_index,18,line[2])
								
							con.TOTAL_SIMULATION_TIME=(line[2]/1000.0)
						
						continue
					
###########################################################################################################################
					else:
						eh.display_error(LINE,line_index,19,line[1])
					
###########################################################################################################################

			elif line[0]=="!SUBCKT":
				if circuit_flag!=0:
					eh.display_error(LINE,line_index,20,circuit_flag)
				subckt_nodes_list=[]
				circuit_flag=2
				
				continue

###########################################################################################################################
				
			elif line[0]=="!END_SUBCKT":
				
				circuit_flag=0
				subckt_nodes_list=[]
				continue
				
###########################################################################################################################
				
			elif line[0]=="!MAINCKT_SETUP":
				if circuit_flag!=0:
					eh.display_error(LINE,line_index,24,circuit_flag)
				
				circuit_flag=3
				
				if len(line[1:])==0:
					eh.display_error(LINE,line_index,25,0)
				
				if line[1]=='time':
					arg=line[2:]
					con.mcktstp_time_flag=1
				
				else:
					arg=line[1:]
				
				main_setup_nodes=arg
				
				if len(arg)==0:
					eh.display_error(LINE,line_index,25,0)
				
				for word in arg:
					if type(word)!=int:
						eh.display_error(LINE,line_index,26,str(word))
					if not(word in nodes_list):
						eh.display_error(LINE,line_index,43,str(word))
						
				con.MAINCKT_SETUP_NODE=line[1:]
		
				continue

###########################################################################################################################
				
			elif line[0]=="!END_MAINCKT_SETUP":
				if circuit_flag!=3:
					eh.display_error(LINE,line_index,27,0)
					
				if len(line)>1:
					try:
						con.MAINCKT_SETUP_FILENAME=str(line[1])
						con.MAINCKT_SETUP_DATA=open(line[1],"r")
					except IOError:
						eh.display_error(LINE,line_index,46,line[1])
					else:
						con.MAINCKT_SETUP_DATA=con.MAINCKT_SETUP_DATA.readlines()
						
						for setup_data_index in range(len(con.MAINCKT_SETUP_DATA)):
							
							con.MAINCKT_SETUP_DATA[setup_data_index]=con.MAINCKT_SETUP_DATA[setup_data_index].split()

							for data_node_index in range(len(con.MAINCKT_SETUP_DATA[setup_data_index])):
								
								if not(eh.is_numeric(con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index])):
									eh.display_error(LINE,line_index,48,(line[1],setup_data_index,con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index]))
								
								con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index]=eval(con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index])
								
								if data_node_index!=0 and con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index]!=0 and con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index]!=1:
									eh.display_error(LINE,line_index,64,(line[1],setup_data_index,con.MAINCKT_SETUP_DATA[setup_data_index][data_node_index]))
									
								
							if len(con.MAINCKT_SETUP_DATA[setup_data_index])!=(len(main_setup_nodes)+con.mcktstp_time_flag):
								eh.display_error(LINE,line_index,47,(line[1],setup_data_index))
								
							con.SETUP_DATA.append(con.MAINCKT_SETUP_DATA[setup_data_index])
							
				circuit_flag=0

				continue
				
###########################################################################################################################
				
			elif line[0]=="!CONNECT_OUT_ARDUINO":
				
				if con.CONNECT_OUT_FLAG==0:
					eh.display_error(LINE,line_index,55,0)
				
				if circuit_flag!=0:
					eh.display_error(LINE,line_index,51,circuit_flag)
				
				if len(line)<3:
					eh.display_error(LINE,line_index,59,(len(line)-1))
					
				con.BOARD_NAME=line[1]
				con.PORT_NAME=line[2]
				
				try:
					con.BOARD_INFO=open(con.PREPATH+"\ARDUINO_BOARD_INFO\\"+line[1]+".txt","r")
				
				except:
					eh.display_error(LINE,line_index,50,line[1])
					
				else:
					
					con.BOARD_INFO=con.BOARD_INFO.readlines()
					
					for info_index in range(len(con.BOARD_INFO)):
						arduino_pin_list.append(con.BOARD_INFO[info_index][:3])
						con.BOARD_OUTPUT.append(["n.c.","n.c.","n.c."])
						con.BOARD_INPUT.append(["n.c.","n.c."])
						
					circuit_flag=4

					continue

###########################################################################################################################

			elif line[0]=="!END_CONNECT_OUT_ARDUINO":
				
				if circuit_flag!=4:
					eh.display_error(LINE,line_index,52,0)
				
				circuit_flag=0
				
				continue
				
###########################################################################################################################
			elif line[0]=="!WRITE_TO_FILE":
				if len(line)!=2:
					eh.display_error(LINE,line_index,60,(len(line)-1))
				con.ANALYSIS_DATA_FILENAME=str(line[1])
				con.ANALYSIS_DATA=open(con.ANALYSIS_DATA_FILENAME,"w")

				continue
###########################################################################################################################
			

			else:
				eh.display_error(LINE,line_index,0,line[0][1:])
			
		elif	line[0]=="$":
				
			if	(len(main_setup_nodes)+con.mcktstp_time_flag)!=len(line[1:]):
				eh.display_error(LINE,line_index,28,0)
				
			for word in line[(1+con.mcktstp_time_flag):]:
				
				if type(word)!=int :
					eh.display_error(LINE,line_index,29,str(word))
				if word < 0 :
					eh.display_error(LINE,line_index,29,str(word))
			
			for word in line[(1+con.mcktstp_time_flag):]:
				if word!=0 and word!=1:
					eh.display_error(LINE,line_index,63,str(word))
			
			if circuit_flag==3:
				con.SETUP_DATA.append(line[1:])

			continue
			
###########################################################################################################################
		
		elif line[0]=="#":
		
			if circuit_flag==4:
				
				if len(line[1:])!=2:
					eh.display_error(LINE,line_index,53,0)
				
				
				temp_node=line[1]
				temp_pin=line[2]
				
				
				if temp_pin[3:]!="=INPUT" and temp_pin[3:]!="=OUTPUT":
					eh.display_error(LINE,line_index,59,temp_pin)
				
					
				if not(temp_node in nodes_list):
					eh.display_error(LINE,line_index,43,temp_node)
				
				
				if not(temp_pin[:3] in arduino_pin_list):
					eh.display_error(LINE,line_index,54,[temp_pin[:3],con.BOARD_NAME])
			
				
				for board_index in range(len(arduino_pin_list)):
					
					if temp_pin[:3]==arduino_pin_list[board_index]:
						if temp_pin[4:]=="OUTPUT":
							con.CONNECT_OUT_NODE_OUT.append(str(temp_node)+'('+str(temp_pin[:3])+')')
							con.BOARD_OUTPUT[board_index][0]=temp_node
						elif temp_pin[4:]=="INPUT":
							con.BOARD_INPUT[board_index][0]=temp_node
							con.CONNECT_OUT_NODE_IN.append(str(temp_node)+'('+str(temp_pin[:3])+')')
			continue				

###########################################################################################################################
	
		elif line[0]=="SUBCKT":
			if len(line)<2:
				eh.display_error(LINE,line_index,30,0)
			
			if type(line[1])!=str:
				eh.display_error(LINE,line_index,30,0)
			
			try:
				temp_file=open(con.PREPATH+"\SUBCIRCUITS_USER_DEFINED\\"+line[1]+".txt","r")
			except	IOError:
				try:
					if line[1][:2]=="IC":
						
						temp_file=open(con.PREPATH+"\IC74XX\\"+line[1]+".txt","r")
					else:
						temp_file=open(con.PREPATH+"\SUBCIRCUITS_INBUILT\\"+line[1]+".txt","r")
				except IOError:
					eh.display_error(LINE,line_index,33,line[1])
			
			temp_data=(temp_file.readlines())[0].split()
			temp_file.close()
				
			if	len(temp_data)!=len(line[2:]):
				eh.display_error(LINE,line_index,34,0)
				
			arg=line[2:]
			
			for word in arg:
				if type(word)!=int:
					eh.display_error(LINE,line_index,42,str(word))
				if word < 0:
					eh.display_error(LINE,line_index,42,str(word))
				if circuit_flag==1:
					nodes_list.append(word)
				elif circuit_flag==2:
					subckt_nodes_list.append(word)
			
			if circuit_flag==1:
				con.MAINCKT_DATA.append(line)
			
			continue

###########################################################################################################################
			
		elif line[0]=="NOT" or line[0]=="BUFFER":
			arg=line[1:]
			
			if circuit_flag!=1 and circuit_flag!=2:
				eh.display_error(LINE,line_index,41,0)
			
			if len(arg)!=2:
				eh.display_error(LINE,line_index,31,0)
			
			for word in arg:
				if type(word)!=int:
					eh.display_error(LINE,line_index,36,str(word))
				if word < 0:
					eh.display_error(LINE,line_index,36,str(word))
				if circuit_flag==1:
					nodes_list.append(word)
				elif circuit_flag==2:
					subckt_nodes_list.append(word)
				
			if circuit_flag==1:
				con.MAINCKT_DATA.append(line)
				
			continue

###########################################################################################################################
		
		elif line[0]=="AND_2" or line[0]=="OR_2" or line[0]=="NAND_2" or line[0]=="NOR_2" or line[0]=="XOR_2" or line[0]=="XNOR_2" or line[0]=="TRISTATE_BUFFER":
			
			arg=line[1:]
			
			if circuit_flag!=1 and circuit_flag!=2:
				eh.display_error(LINE,line_index,41,0)
			
			if len(arg)!=3:
				eh.display_error(LINE,line_index,37,len(arg))
				
			
			for word in arg:
				if type(word)!=int:
					eh.display_error(LINE,line_index,38,str(word))
				if word < 0:
					eh.display_error(LINE,line_index,38,str(word))
				if circuit_flag==1:
					nodes_list.append(word)
				elif circuit_flag==2:
					subckt_nodes_list.append(word)
				
			if circuit_flag==1:
				con.MAINCKT_DATA.append(line)
			
			continue

###########################################################################################################################
		elif line[0]=="ND":
		
			arg=line[1:]
			
			if circuit_flag!=1 and circuit_flag!=2:
				eh.display_error(LINE,line_index,41,0)
		
			for word in arg:
				if type(word)!=int:
					eh.display_error(LINE,line_index,38,str(word))
				if word < 0:
					eh.display_error(LINE,line_index,38,str(word))
				if circuit_flag==1:
					nodes_list.append(word)
				elif circuit_flag==2:
					subckt_nodes_list.append(word)
		
			if circuit_flag==1:
				con.MAINCKT_DATA.append(line)
			
			continue
###########################################################################################################################
		
		else:
			eh.display_error(LINE,line_index,32,LINE)
	
	if circuit_flag!=0:
		eh.display_error(SCRIPT[-1]+"\n",length,39,circuit_flag)
	
###########################################################################################################################