import config as con
from string import *
from datetime import datetime

def toStr(a_list):
	if len(a_list)==0:
		return ["n.n."]
	for i in range(len(a_list)):
		a_list[i]=str(a_list[i])
	return a_list
	
def checkFile(file_name):
	if file_name=="" or file_name==None:
		return "n.f."
	return file_name
	
def display_start_data():
	print "\nFile creation timestamp -",datetime.now()
	print "ZEBRA v3.3 (v3.3.0, February 28, 2021)"
	print "Refer to the user manual for more information\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\nFile creation timestamp - "+str(datetime.now())+"\n")
		con.ANALYSIS_DATA.write("ZEBRA v3.3 (v3.3.0, February 28, 2021)\n")
		con.ANALYSIS_DATA.write( "Refer to the user manual for more information\n\n")
	
def set_flag(a_value):
	if a_value!=[]:
		return 'yes'
	else:
		return 'no'
	
def SETUP_ANALYSIS_data_display():
	print "-Starting pre simulation setup analysis-"
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("-Starting pre simulation setup analysis-\n")
	
def OT_ANALYSIS_data_display():
	
	print "\n*****************************************************************\n"
	print "-analysis type : OT_ANALYSIS"
	print "-number of nodes to be analysed :",len(con.NODE_DATA)
	print "-nodes to be scanned :",join(toStr(con.SCAN_NODE),',')
	print "-nodes to be printed :",join(toStr(con.PRINT_NODE),',')
	print "-nodes connected out :",join(toStr(con.CONNECT_OUT_NODE_OUT),',')
	print "-nodes connected in :",join(toStr(con.CONNECT_OUT_NODE_IN),',')
	print "-data file name to be written to :",checkFile(con.ANALYSIS_DATA_FILENAME)
	print "\n*****************************************************************\n"
	print "-pre-simulation setup :",set_flag(con.MAINCKT_SETUP_NODE)
	print "-pre-simulation setup file :",checkFile(con.MAINCKT_SETUP_FILENAME)
	print "-pre-simulation setup nodes :",join(toStr(con.MAINCKT_SETUP_NODE),',')
	print "-pre-simulation setup cycles :",len(con.SETUP_DATA)
	print "\n*****************************************************************\n"
	print "-the simulation calculates the bias point voltages at the nodes"
	print "-the node voltages will be printed under the node names"
	print "\n*****************************************************************\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-analysis type : OT_ANALYSIS\n")
		con.ANALYSIS_DATA.write("-number of nodes to be analysed :"+str(len(con.NODE_DATA))+"\n")
		con.ANALYSIS_DATA.write("-nodes to be scanned :"+join(toStr(con.SCAN_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes to be printed :"+join(toStr(con.PRINT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected out :"+join(toStr(con.CONNECT_OUT_NODE_OUT),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected in :"+join(toStr(con.CONNECT_OUT_NODE_IN),',')+"\n")
		con.ANALYSIS_DATA.write("-data file name to be written to :"+checkFile(con.ANALYSIS_DATA_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup :"+set_flag(con.MAINCKT_SETUP_NODE)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup file :"+checkFile(con.MAINCKT_SETUP_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup nodes :"+join(toStr(con.MAINCKT_SETUP_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup cycles :"+str(len(con.SETUP_DATA))+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-the simulation calculates the bias point voltages at the nodes\n")
		con.ANALYSIS_DATA.write("-the node voltages will be printed under the node names\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		
def RT_ANALYSIS_data_display():
	print "\n*****************************************************************\n"
	print "-analysis type : RT_ANALYSIS"
	print "-number of nodes to be analysed :",len(con.NODE_DATA)
	print "-nodes to be scanned :",join(toStr(con.SCAN_NODE),',')
	print "-nodes to be printed :",join(toStr(con.PRINT_NODE),',')
	print "-nodes to be plotted :",join(toStr(con.PLOT_NODE),',')
	print "-nodes connected out :",join(toStr(con.CONNECT_OUT_NODE_OUT),',')
	print "-nodes connected in :",join(toStr(con.CONNECT_OUT_NODE_IN),',')
	print "\n*****************************************************************\n"
	print "-pre-simulation setup :",set_flag(con.MAINCKT_SETUP_NODE)
	print "-pre-simulation setup file :",checkFile(con.MAINCKT_SETUP_FILENAME)
	print "-pre-simulation setup nodes :",join(toStr(con.MAINCKT_SETUP_NODE),',')
	print "-pre-simulation setup cycles :",len(con.SETUP_DATA)
	print "\n*****************************************************************\n"
	print "-the simulation takes place in real time"
	print "-both printing and plotting of data will take place in a seperate window"
	print "-the node voltages will be printed under the node names"
	print "-the node voltages are updated in real time"
	print "-scanning node voltages takes place in the cmd window"
	print "-Simply press enter without providing any node voltages to exit simulation"
	print "\n*****************************************************************\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-analysis type : RT_ANALYSIS\n")
		con.ANALYSIS_DATA.write("-number of nodes to be analysed :"+str(len(con.NODE_DATA))+"\n")
		con.ANALYSIS_DATA.write("-nodes to be scanned :"+join(toStr(con.SCAN_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes to be printed :"+join(toStr(con.PRINT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes to be plotted :"+join(toStr(con.PLOT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected out :"+join(toStr(con.CONNECT_OUT_NODE_OUT),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected in :"+join(toStr(con.CONNECT_OUT_NODE_IN),',')+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup :"+set_flag(con.MAINCKT_SETUP_NODE)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup file :"+checkFile(con.MAINCKT_SETUP_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup nodes :"+join(toStr(con.MAINCKT_SETUP_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup cycles :"+str(len(con.SETUP_DATA))+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-the simulation takes place in real time\n")
		con.ANALYSIS_DATA.write("-both printing and plotting of data will take place in a seperate window\n")
		con.ANALYSIS_DATA.write("-the node voltages will be printed under the node names\n")
		con.ANALYSIS_DATA.write("-the node voltages are updated in real time\n")
		con.ANALYSIS_DATA.write("-scanning node voltages takes place in the cmd window\n")
		con.ANALYSIS_DATA.write("-Simply press enter without providing any node voltages to exit simulation\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		
def TT_ANALYSIS_data_display():
	print "\n*****************************************************************\n"
	print "-analysis type : TT_ANALYSIS"
	print "-number of nodes to be analysed :",len(con.NODE_DATA)
	print "-input nodes :",join(toStr(con.INPUT_NODE),',')
	print "-nodes connected out :",join(toStr(con.CONNECT_OUT_NODE_OUT),',')
	print "-nodes connected in :",join(toStr(con.CONNECT_OUT_NODE_IN),',')
	print "-data file name to be read from :",checkFile(con.TRUTH_TABLE_INPUT_DATA_FILENAME)
	print "-data file name to be written to :",checkFile(con.ANALYSIS_DATA_FILENAME)
	print "\n*****************************************************************\n"
	print "-pre-simulation setup :",set_flag(con.MAINCKT_SETUP_NODE)
	print "-pre-simulation setup file :",checkFile(con.MAINCKT_SETUP_FILENAME)
	print "-pre-simulation setup nodes :",join(toStr(con.MAINCKT_SETUP_NODE),',')
	print "-pre-simulation setup cycles :",len(con.SETUP_DATA)
	print "\n*****************************************************************\n"
	print "-performs RT_ANALYSIS for predefined input values"
	print "-the node voltages will be printed under the node names"
	print "\n*****************************************************************\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-analysis type : TT_ANALYSIS\n")
		con.ANALYSIS_DATA.write("-number of nodes to be analysed :"+str(len(con.NODE_DATA))+"\n")
		con.ANALYSIS_DATA.write("-input nodes :"+join(toStr(con.INPUT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-output nodes :"+join(toStr(con.OUTPUT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected out :"+join(toStr(con.CONNECT_OUT_NODE_OUT),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected in :"+join(toStr(con.CONNECT_OUT_NODE_IN),',')+"\n")
		con.ANALYSIS_DATA.write("-data file name to be read from :"+checkFile(con.TRUTH_TABLE_INPUT_DATA_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("-data file name to be written to :"+checkFile(con.ANALYSIS_DATA_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup :"+set_flag(con.MAINCKT_SETUP_NODE)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup file :"+checkFile(con.MAINCKT_SETUP_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup nodes :"+join(toStr(con.MAINCKT_SETUP_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup cycles :"+str(len(con.SETUP_DATA))+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-performs RT_ANALYSIS for predefined input values\n")
		con.ANALYSIS_DATA.write("-the node voltages will be printed under the node names\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")

def TIME_ANALYSIS_data_display():
	print "\n*****************************************************************\n"
	print "-analysis type : TIME_ANALYSIS"
	print "-number of nodes to be analysed :",len(con.NODE_DATA)
	print "-nodes to be scanned :",join(toStr(con.SCAN_NODE),',')
	print "-nodes to be printed :",join(toStr(con.PRINT_NODE),',')
	print "-nodes to be plotted :",join(toStr(con.PLOT_NODE),',')
	print "-nodes connected out :",join(toStr(con.CONNECT_OUT_NODE_OUT),',')
	print "-nodes connected in :",join(toStr(con.CONNECT_OUT_NODE_IN),',')
	print "-data file name to be written to :",checkFile(con.ANALYSIS_DATA_FILENAME)
	print "\n*****************************************************************\n"
	print "-pre-simulation setup :",set_flag(con.MAINCKT_SETUP_NODE)
	print "-pre-simulation setup file :",checkFile(con.MAINCKT_SETUP_FILENAME)
	print "-pre-simulation setup nodes :",join(toStr(con.MAINCKT_SETUP_NODE),',')
	print "-pre-simulation setup cycles :",len(con.SETUP_DATA)
	print "\n*****************************************************************\n"
	print "-performs real time simulation for predefined input values"
	print "-plotting of data will take place in a seperate window"
	print "-the node voltages will be printed in cmd window"
	print "-the node voltages are updated in real time"
	print "-Simply press enter to exit simulation"
	print "\n*****************************************************************\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-analysis type : TIME_ANALYSIS\n")
		con.ANALYSIS_DATA.write("-number of nodes to be analysed :"+str(len(con.NODE_DATA))+"\n")
		con.ANALYSIS_DATA.write("-nodes to be scanned :"+join(toStr(con.SCAN_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes to be printed :"+join(toStr(con.PRINT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes to be plotted :"+join(toStr(con.PLOT_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected out :"+join(toStr(con.CONNECT_OUT_NODE_OUT),',')+"\n")
		con.ANALYSIS_DATA.write("-nodes connected in :"+join(toStr(con.CONNECT_OUT_NODE_IN),',')+"\n")
		con.ANALYSIS_DATA.write("-data file name to be written to :"+checkFile(con.ANALYSIS_DATA_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup :"+set_flag(con.MAINCKT_SETUP_NODE)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup file :"+checkFile(con.MAINCKT_SETUP_FILENAME)+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup nodes :"+join(toStr(con.MAINCKT_SETUP_NODE),',')+"\n")
		con.ANALYSIS_DATA.write("-pre-simulation setup cycles :"+str(len(con.SETUP_DATA))+"\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
		con.ANALYSIS_DATA.write("-performs real time simulation for predefined input values\n")
		con.ANALYSIS_DATA.write("-plotting of data will take place in a seperate window\n")
		con.ANALYSIS_DATA.write("-the node voltages will be printed in cmd window\n")
		con.ANALYSIS_DATA.write("-the node voltages are updated in real time\n")
		con.ANALYSIS_DATA.write("-Simply press enter to exit simulation\n")
		con.ANALYSIS_DATA.write("\n####################################################################################################################################\n\n")
			
	
	
	
def detdisplay_ANALYSIS_data():
	if con.ANALYSIS=='OT_ANALYSIS':
		OT_ANALYSIS_data_display()
	elif con.ANALYSIS=='RT_ANALYSIS':
		RT_ANALYSIS_data_display()
	if con.ANALYSIS=='TT_ANALYSIS':
		TT_ANALYSIS_data_display()
	if con.ANALYSIS=='TIME_ANALYSIS':
		TIME_ANALYSIS_data_display()
	
def start_sim():
	if con.MAINCKT_SETUP_NODE!=[]:
		print "\n-PRE-SIMULATION SETUP ENDED-\n"
		if con.ANALYSIS_DATA!=None:
			con.ANALYSIS_DATA.write("\n-PRE-SIMULATION SETUP ENDED-\n\n")
	
	_=raw_input("-press enter to start simulation...")
	print ""
	print "-STARTING SIMULATION-\n"
	
	if con.ANALYSIS_DATA!=None:
		con.ANALYSIS_DATA.write("-STARTING SIMULATION-\n\n")
	
def start_mcktstp_sim():
	if con.MAINCKT_SETUP_NODE!=[]:
		_=raw_input("-press enter to start pre-simulation setup...")
		print ""
		print "-STARTING PRE-SIMULATION SETUP-\n"
		
		if con.ANALYSIS_DATA!=None:
			con.ANALYSIS_DATA.write("-STARTING PRE-SIMULATION SETUP-\n\n")