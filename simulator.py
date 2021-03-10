import config as con
import gates as gt
import construct_circuit as cc
import read_code as rc
import plot_data as pd
import error_handle as eh
import arducom as ad
import subcircuit_definition as sd
import functional_node_sort as fns
import analysis_data as analyd
import time
import thread
import threading
import os
import analysis_data as analyd
import turtle

##########################################################################################################################

def stop_thread(thread):
	thread.join()
	con.circuit_simulation_flag=False
	con.end_time=time.clock()

##########################################################################################################################

def clocking():
	con.current_time=time.clock()
	
	if con.CLOCK_DATA!=None:
		if con.CLOCK_DATA[5]==0:
			if (con.current_time-con.last_time)>=con.CLOCK_DATA[1]:
				con.CLOCK_DATA[5]=1
				con.last_time=con.current_time
		else:
			if con.CLOCK_DATA[4]==0:
				if (con.current_time-con.last_time)>=con.CLOCK_DATA[3]:
					con.CLOCK_DATA[4]=1
					con.NODE_DATA[con.CLOCK_DATA[0]][2]=con.CLOCK_DATA[4]
					con.last_time=con.current_time
			else:
				if (con.current_time-con.last_time)>=con.CLOCK_DATA[2]:
					con.CLOCK_DATA[4]=0
					con.NODE_DATA[con.CLOCK_DATA[0]][2]=con.CLOCK_DATA[4]
						
					con.last_time=con.current_time

###########################################################################################################################

def clock_flaging(a_time):
	con.current_time=time.clock()
	elapsed_time=con.current_time-con.start_time
	if (elapsed_time*1000)>=a_time:
		return True
	else:
		return False

###########################################################################################################################

def real_time_circuit_simulation(lock):
	try:
		while con.circuit_simulation_flag:
			
			clocking()
			lock.acquire()
			simulator()
			lock.release()
			if con.PRINT_NODE_INDEX!=[]:
				pd.real_time_print()
				
			elif con.PLOT_NODE!=[]:
				
				temp_data_plot=[]	
				temp_data_plot.append(con.current_time-con.start_time)
				
				for plot_node_index in con.PLOT_NODE_INDEX:
					temp_data_plot.append(int(con.NODE_DATA[plot_node_index][-1]))
				
				pd.animate_plot_nodes(temp_data_plot)
		
	except:
		con.circuit_simulation_flag=False

###########################################################################################################################

def circuit_simulation(lock):
	try:
		while con.circuit_simulation_flag:
			
			lock.acquire()
			simulator()
			lock.release()
		
	except:
		con.circuit_simulation_flag=False
	
###########################################################################################################################

def arduino_python_serial_communication_in(lock):
	try:
		while con.serial_communication_flag:
			ad.arduino2python(lock)

	except:
		exit()
			
###########################################################################################################################

def arduino_python_serial_communication_out(lock):
	try:
		while con.serial_communication_flag:
			ad.python2arduino(lock)

	except:
		exit()
			
###########################################################################################################################
			
def input_thread(a_list):
	raw_input()
	a_list.append(True)
	con.end_time=time.clock()

###########################################################################################################################

def gate_operate(gate,NODE_DATA):
	if gate[0]=="BUFFER":
		NODE_DATA[gate[2]][2]=gt.BUFFER(NODE_DATA[gate[1]][2])
	elif gate[0]=="TRISTATE_BUFFER":
		NODE_DATA[gate[3]][2]=gt.TRISTATE_BUFFER(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2],NODE_DATA[gate[3]][2])
	elif gate[0]=="AND_2":
		NODE_DATA[gate[3]][2]=gt.AND_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	elif gate[0]=="OR_2":
		NODE_DATA[gate[3]][2]=gt.OR_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	elif gate[0]=="NOT":
		NODE_DATA[gate[2]][2]=gt.NOT(NODE_DATA[gate[1]][2])
	elif gate[0]=="NAND_2":
		NODE_DATA[gate[3]][2]=gt.NAND_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	elif gate[0]=="NOR_2":
		NODE_DATA[gate[3]][2]=gt.NOR_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	elif gate[0]=="XOR_2":
		NODE_DATA[gate[3]][2]=gt.XOR_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	elif gate[0]=="XNOR_2":
		NODE_DATA[gate[3]][2]=gt.XNOR_2(NODE_DATA[gate[1]][2],NODE_DATA[gate[2]][2])
	
	return NODE_DATA

###########################################################################################################################

def input_values_generator(INPUT_VARIABLES_COUNT):
	
	INPUT_DATA=[]
	
	for count in range(2**INPUT_VARIABLES_COUNT):
		binary=bin(count)
		binary=list(binary)
		binary=binary[2:]
		
		for b in range(len(binary)):
			binary[b]=eval(binary[b])
		for b in range(INPUT_VARIABLES_COUNT-len(binary)):
			binary.insert(0,0)
		
		INPUT_DATA.append(binary)
		
	return INPUT_DATA

###########################################################################################################################

def simulator():
	
	for gate in con.MAINCKT_DATA:
		con.NODE_DATA=gate_operate(gate,con.NODE_DATA)
	

	for tb_index in con.tristate_buffer_list:
		set_op0_flag=1
		tb_enable_list=tb_index[1:]
					
		for tb_en_index	in tb_enable_list:
			if con.NODE_DATA[tb_en_index][2]==1:
				set_op0_flag=0
				break
	
		if set_op0_flag==1:
			con.NODE_DATA[tb_index[0]][2]=0
	
	temp_connect_out_buff_data=0
	if con.BOARD_INFO!=None and con.tristate_buffer_list!=[]: 
		for pin_index in con.BOARD_OUTPUT:
			if pin_index[2]=='n.c.':
				temp_connect_out_buff_data=temp_connect_out_buff_data<1
			else:
				temp_flag=True
				for tb_en in pin_index[2]:
					if con.NODE_DATA[tb_en][2]==1:
						temp_flag=False
						break
				if temp_flag==True:
					temp_connect_out_buff_data=(temp_connect_out_buff_data<1) | 1
				else:
					temp_connect_out_buff_data=temp_connect_out_buff_data<1
		con.DDR_DATA=con.ddr_DATA & (temp_connect_out_buff_data ^ 65535)
		
	else:
		con.DDR_DATA=con.ddr_DATA

def main():
###########################################################################################################################

	con.initialize()
	sd.def_subckt()
	rc.scan_code(con.CODE_DATA)
	cc.circuit_construct()
	fns.functional_indexing()

###########################################################################################################################

	analyd.display_start_data()

###########################################################################################################################

	if con.BOARD_INFO!=None:
		ad.initialize_arducom()

###########################################################################################################################

	lock=threading.Lock()
	circuit_simulation_thread=threading.Thread(target=circuit_simulation,args=(lock,))
	real_time_circuit_simulation_thread=threading.Thread(target=real_time_circuit_simulation,args=(lock,))
	arduino_python_serial_communication_in_thread=threading.Thread(target=arduino_python_serial_communication_in,args=(lock,))
	arduino_python_serial_communication_out_thread=threading.Thread(target=arduino_python_serial_communication_out,args=(lock,))
	clocking_thread=threading.Thread(target=clocking)

###########################################################################################################################

	if con.BOARD_INFO!=None:
		arduino_python_serial_communication_in_thread.start()
		arduino_python_serial_communication_out_thread.start()

	if con.scan_sampling_time<0.03:
		con.scan_sampling_time=0.03

###########################################################################################################################	

	analyd.detdisplay_ANALYSIS_data()
	analyd.start_mcktstp_sim()

###########################################################################################################################	

	if con.MAINCKT_SETUP_NODE_INDEX!=[]:
		
		if con.ANALYSIS_DATA==None:
			
			for i in  con.PRINT_NODE:
				if i !='time':
					print i,"\t",
				else:
					print "ms.\t",
			
			print ""

		else:
			mcktstp_file_data=""
				
			for i in con.PRINTF_NODE:
				if i !='time':
					mcktstp_file_data=mcktstp_file_data+str(i)+"\t"
				else:
					mcktstp_file_data=mcktstp_file_data+"ms.\t"
			
			con.ANALYSIS_DATA.write(mcktstp_file_data+"\n")

	mcktstp_index=0

	con.start_time=time.clock()
	con.last_time=con.start_time

###########################################################################################################################	

	while con.MAINCKT_SETUP_NODE_INDEX!=[] and con.SETUP_DATA!=[]:
		if con.mcktstp_time_flag==1:
			
			if clock_flaging(con.SETUP_DATA[mcktstp_index+1][0]):
				mcktstp_index+=1
				
				if mcktstp_index==(len(con.SETUP_DATA)-1):
					break
		
		else:
			con.current_time=time.clock()
			if (con.current_time-con.last_time)>=con.scan_sampling_time:
				mcktstp_index+=1
				con.last_time=con.current_time
				
				if mcktstp_index==len(con.SETUP_DATA):
					break
		
		lock.acquire()
		for input_index in range(len(con.MAINCKT_SETUP_NODE_INDEX)):
			con.NODE_DATA[con.MAINCKT_SETUP_NODE_INDEX[input_index]][2]=con.SETUP_DATA[mcktstp_index][input_index+con.mcktstp_time_flag]
		lock.release()
		
		temp_data_print=[]
		mcktstp_file_data=""
		
		simulator()
		
		if con.BOARD_INFO!=None:
			time.sleep(con.serial_sync_time)

		if con.ANALYSIS_DATA==None:
			for mainckt_setup_index in con.PRINT_NODE_INDEX:
				if mainckt_setup_index!='time':
					temp_data_print.append(int(con.NODE_DATA[mainckt_setup_index][-1]))
				else:
					temp_data_print.append(round((con.current_time*1000),1))
		else:
			for mainckt_setup_index in con.PRINTF_NODE_INDEX:
				if mainckt_setup_index!='time':
					mcktstp_file_data=mcktstp_file_data+str((int(con.NODE_DATA[mainckt_setup_index][-1])))+"\t"
				else:
					mcktstp_file_data=mcktstp_file_data+str(round((con.current_time*1000),1))+"\t"
		
		if con.ANALYSIS_DATA==None:
			con.MAINCKT_PRINT_ARRAY.append(temp_data_print)
		else:
			con.ANALYSIS_DATA.write(mcktstp_file_data+"\n")

###########################################################################################################################

	if con.PRINT_NODE!=[]:
		for display_data in con.MAINCKT_PRINT_ARRAY:
			for data in display_data:
				print data,"\t",
			print ""

###########################################################################################################################

	analyd.start_sim()

###########################################################################################################################

	if con.ANALYSIS=="TT_ANALYSIS":
		
		con.MAXIMUM_SIMULATION_COUNT=1
		if con.TRUTH_TABLE_INPUT_DATA_FILE==None:
			con.INPUT_VARIABLES_VALUE=input_values_generator(con.INPUT_VARIABLES_COUNT)
		
		con.start_time=time.clock()
###########################################################################################################################
		
		if con.tt_time_flag==0:
		
###########################################################################################################################
			if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
				time_file_data=''
				
				for i in con.PRINTF_NODE:
					if i != 'time':
						time_file_data=time_file_data+str(i)+"\t"
					else:
						time_file_data=time_file_data+"ms.\t"

				con.ANALYSIS_DATA.write(time_file_data+"\n")
			
			if con.PRINT_NODE!=[]:
				temp_data_print=[]
				for i in con.PRINT_NODE:
					if i != 'time':
						temp_data_print.append(i)
					else:
						temp_data_print.append('ms.')
				
				con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
			
			for tt_index in range(len(con.INPUT_VARIABLES_VALUE)):
				
				for input_index in range(len(con.INPUT_NODE_INDEX)):
					con.NODE_DATA[con.INPUT_NODE_INDEX[input_index]][2]=con.INPUT_VARIABLES_VALUE[tt_index][input_index]
				simulator()
				
				if con.BOARD_INFO!=None:
					time.sleep(con.scan_sampling_time)
				
				temp_data_print=[]
				con.current_time=time.clock()
				
				lock.acquire()
				for print_node_index in con.PRINT_NODE_INDEX:
					if print_node_index!='time':
						temp_data_print.append(int(con.NODE_DATA[print_node_index][-1]))
					else:
						temp_data_print.append(round(((con.current_time-con.start_time)*1000),1))
				lock.release()
				
				if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
					time_file_data=""
				
					lock.acquire()
					for printf_node_index in con.PRINTF_NODE_INDEX:
						if printf_node_index!='time':
							time_file_data=time_file_data+str(int(con.NODE_DATA[printf_node_index][-1]))+"\t"
						else:
							time_file_data=time_file_data+str(round(((con.current_time-con.start_time)*1000),1))+"\t"
					lock.release()
					
					con.ANALYSIS_DATA.write(time_file_data+"\n")
				
				con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
				
			
			con.end_time=time.clock()
				
###########################################################################################################################
		
		else:
			con.start_time=time.clock()
			con.last_time=con.start_time
			
			circuit_simulation_thread.start()
			
###########################################################################################################################
			
			temp_data_print=[]			
			
			if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
				time_file_data=''
			
				for i in con.PRINTF_NODE:
					if i != 'time':
						time_file_data=time_file_data+str(i)+"\t"
					else:
						time_file_data=time_file_data+"ms.\t"

				con.ANALYSIS_DATA.write(time_file_data+"\n")
		
			if con.PRINT_NODE!=[]:
				temp_data_print=[]
				for i in con.PRINT_NODE:
					if i != 'time':
						temp_data_print.append(i)
					else:
						temp_data_print.append('ms.')
				
			con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
		
			tt_index=0
			
###########################################################################################################################	
				
			while con.circuit_simulation_flag:
				
				if clock_flaging(con.INPUT_VARIABLES_VALUE[tt_index+1][0]):
					tt_index+=1
					
					if tt_index==(len(con.INPUT_VARIABLES_VALUE)-1):
						con.end_time=time.clock()
						con.circuit_simulation_flag=False
						circuit_simulation_thread.join()
						break
				lock.acquire()
				for input_index in range(len(con.INPUT_NODE_INDEX)):
					con.NODE_DATA[con.INPUT_NODE_INDEX[input_index]][2]=con.INPUT_VARIABLES_VALUE[tt_index][input_index+con.tt_time_flag]
				lock.release()
			
				if con.BOARD_INFO!=None:
					time.sleep(con.serial_sync_time)
				
###########################################################################################################################	

				temp_data_print=[]
				temp_data_plot=[]
				
				temp_data_plot.append(con.current_time-con.start_time)
			
				lock.acquire()
				for print_node_index in con.PRINT_NODE_INDEX:
					if print_node_index!='time':
						temp_data_print.append(int(con.NODE_DATA[print_node_index][-1]))
					else:
						temp_data_print.append(round(((con.current_time-con.start_time)*1000),1))
					
				for plot_node_index in con.PLOT_NODE_INDEX:
					temp_data_plot.append(int(con.NODE_DATA[plot_node_index][-1]))
				lock.release()
				
				if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
					time_file_data=""
				
					lock.acquire()
					for printf_node_index in con.PRINTF_NODE_INDEX:
						if printf_node_index!='time':
							time_file_data=time_file_data+str(int(con.NODE_DATA[printf_node_index][-1]))+"\t"
						else:
							time_file_data=time_file_data+str(round(((con.current_time-con.start_time)*1000),1))+"\t"
					lock.release()
					
					con.ANALYSIS_DATA.write(time_file_data+"\n")
				
				con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
				con.PLOT_DATA.append(temp_data_plot)
			
###########################################################################################################################	
		
		if con.PRINT_NODE!=[]:
			
			for display_data in con.TIME_ANALYSIS_DATA_ARRAY:
				for data in display_data:
					print data,"\t",
				print ""
			
		if con.PLOT_NODE!=[] and con.tt_time_flag!=0:
			pd.plot_nodes()

###########################################################################################################################	

	elif con.ANALYSIS=="OT_ANALYSIS":
		
		con.MAXIMUM_SIMULATION_COUNT=5
		
		if con.SCAN_NODE!=[]:
			print "\n-Scanning Node Voltages-\n"
		
		for scan_node_index in con.SCAN_NODE_INDEX:
			temp_store=raw_input(str(con.NODE_DATA[scan_node_index][0])+" : ")
		
			if con.is_number(temp_store):
				temp_store=eval(temp_store)
				if temp_store!=0 and temp_store!=1:
					eh.display_error(0,0,-1,temp_store)
				else:
					con.NODE_DATA[scan_node_index][2]=temp_store
			else:
				eh.display_error(con.ANALYSIS,0,-2,temp_store)
				
		con.start_time=time.clock()
		
		if con.PRINT_NODE!=[]:
			print "\n-Printing Node Voltages-\n"
		
		
		for i in con.PRINT_NODE:
			if i != 'time':
				print i,'\t',
			else:
				print 'ms.','\t',
			
		print ""
		
		for simulation_counter in range(con.MAXIMUM_SIMULATION_COUNT):
			time.sleep(con.scan_sampling_time)
			simulator()
		
		con.end_time=time.clock()
		
		
		for print_node_index in con.PRINT_NODE_INDEX:
			if print_node_index != 'time':
				print int(con.NODE_DATA[print_node_index][-1]),'\t',
			else:
				print round(((time.clock()-con.start_time)*1000),1),'\t',
				
		print "\n"
		
		if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
			temp_data_print=""
			
			for i in con.PRINTF_NODE:
				temp_data_print=temp_data_print+str(i)+'\t'
			
			temp_data_print=temp_data_print+'\n'
			
			for printf_node_index in con.PRINTF_NODE_INDEX:
				temp_data_print=temp_data_print+str(int(con.NODE_DATA[printf_node_index][-1]))+'\t'
			
			con.ANALYSIS_DATA.write(temp_data_print+'\n')

		
###########################################################################################################################

	elif con.ANALYSIS=="RT_ANALYSIS":
		
		con.start_time=time.clock()
		con.last_time=con.start_time
		
		con.MAXIMUM_SIMULATION_COUNT=1
		
		if con.PRINT_NODE!=[]:
			pd.real_time_print_setup()
		
		elif con.PLOT_NODE!=[]:
			pd.animate_plot_nodes_setup()
		
		real_time_circuit_simulation_thread.start()
		
###########################################################################################################################
		scan_cycle_counter=1
		
		while con.circuit_simulation_flag:
			
			if con.SCAN_NODE!=[]:
				print "\n-Scanning Node Voltages-\n"
				print "# Scan cycle :",scan_cycle_counter
			
				for scan_node_index in con.SCAN_NODE_INDEX:
					temp_store=raw_input(str(con.NODE_DATA[scan_node_index][0])+" : ")
					
					if not(con.circuit_simulation_flag):
						eh.display_error(0,0,-6,0)
					
					elif con.is_number(temp_store):
						temp_store=eval(temp_store)
						if temp_store!=0 and temp_store!=1:
							con.circuit_simulation_flag=False
							real_time_circuit_simulation_thread.join()
							con.end_time=time.clock()
							eh.display_error(0,0,-1,temp_store)
						else:
							con.NODE_DATA[scan_node_index][2]=temp_store
					
					else:
						if temp_store=='':
							con.circuit_simulation_flag=False
							real_time_circuit_simulation_thread.join()
							con.end_time=time.clock()
							break
						else:
							con.circuit_simulation_flag=False
							real_time_circuit_simulation_thread.join()
							con.end_time=time.clock()
							eh.display_error(con.ANALYSIS,0,-2,temp_store)
				
			else:
				_=raw_input()
				if not(con.circuit_simulation_flag):
					eh.display_error(0,0,-6,0)
			
				con.circuit_simulation_flag=False
				real_time_circuit_simulation_thread.join()
				con.end_time=time.clock()
				break
				
			scan_cycle_counter+=1
			
			time.sleep(con.scan_sampling_time)
		
###########################################################################################################################
		
	elif con.ANALYSIS=="TIME_ANALYSIS":
		
		con.MAXIMUM_SIMULATION_COUNT=1
		con.start_time=time.clock()
		con.last_time=con.start_time
		con.current_time=con.start_time
		
###########################################################################################################################

		if con.TOTAL_SIMULATION_TIME==None:
			
			if con.PLOT_NODE!=[]:
				pd.animate_plot_nodes_setup()
			
			a_list=[]
			thread.start_new_thread(input_thread,(a_list,))
			
###########################################################################################################################
			
			while not a_list:
				
				lock.acquire()
				
				clocking()
				simulator()
				
				lock.release()
				
				if con.PLOT_NODE!=[]:
					temp_data_plot=[]	
					temp_data_plot.append(con.current_time-con.start_time)
					
					lock.acquire()
					for plot_node_index in con.PLOT_NODE_INDEX:
						temp_data_plot.append(int(con.NODE_DATA[plot_node_index][-1]))
					lock.release()
					pd.animate_plot_nodes(temp_data_plot)
					
					
				if con.PRINT_NODE!=[]:
					lock.acquire()
					
					for print_node_index in con.PRINT_NODE_INDEX:
						if print_node_index!='time':
							print int(con.NODE_DATA[print_node_index][-1]),"\t",
						else:
							print round(((con.current_time-con.start_time)*1000),1),"\t",
					lock.release()
					print ""
				
###########################################################################################################################

		else:
			
			if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
				time_file_data=''
				
				for i in con.PRINTF_NODE:
					if i != 'time':
						time_file_data=time_file_data+str(i)+"\t"
					else:
						time_file_data=time_file_data+"ms.\t"

				con.ANALYSIS_DATA.write(time_file_data+"\n")
			
			if con.PRINT_NODE!=[]:
				temp_data_print=[]
				for i in con.PRINT_NODE:
					if i != 'time':
						temp_data_print.append(i)
					else:
						temp_data_print.append('ms.')
				
				con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
			
			while True:
				
				clocking()
				simulator()
				
				temp_data_print=[]
				temp_data_plot=[]
				
				if con.BOARD_INFO!=None:
					time.sleep(con.serial_sync_time)
				
				temp_data_plot.append(con.current_time-con.start_time)
				
				for print_node_index in con.PRINT_NODE_INDEX:
					if print_node_index!='time':
						temp_data_print.append(int(con.NODE_DATA[print_node_index][-1]))
					else:
						temp_data_print.append(round(((con.current_time-con.start_time)*1000),1))
					
				for plot_node_index in con.PLOT_NODE_INDEX:
					temp_data_plot.append(int(con.NODE_DATA[plot_node_index][-1]))
				
				
				if con.ANALYSIS_DATA!=None and con.PRINTF_NODE!=[]:
					time_file_data=""
			
					for printf_node_index in con.PRINTF_NODE_INDEX:
						if printf_node_index!='time':
							time_file_data=time_file_data+str(int(con.NODE_DATA[printf_node_index][-1]))+"\t"
						else:
							time_file_data=time_file_data+str(round(((con.current_time-con.start_time)*1000),1))+"\t"
							
					con.ANALYSIS_DATA.write(time_file_data+"\n")
				
				con.TIME_ANALYSIS_DATA_ARRAY.append(temp_data_print)
				con.PLOT_DATA.append(temp_data_plot)
				
				if (con.current_time-con.start_time)>=con.TOTAL_SIMULATION_TIME:
					con.end_time=time.clock()
					break
				
			if con.PRINT_NODE!=[]:
				for display_data in con.TIME_ANALYSIS_DATA_ARRAY:
					for data in display_data:
						print data,"\t",
					print ""
				
			if con.PLOT_NODE!=[]:
				pd.plot_nodes()
				
			
###########################################################################################################################
	
	con.clocking_flag=False
	con.circuit_simulation_flag=False	
	con.serial_communication_flag=False

	print "-SIMULATION ENDED-"
	print "-total simulation time :",((con.end_time-con.start_time)*1000),'ms'

	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\n-SIMULATION ENDED-\n")
		con.ANALYSIS_DATA.write("-total simulation time :"+str((con.end_time-con.start_time)*1000)+' ms')
		con.ANALYSIS_DATA.close()
		
	_=raw_input()

###########################################################################################################################
main()
