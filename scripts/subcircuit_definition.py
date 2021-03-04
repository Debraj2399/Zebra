import error_handle as eh
import config as con
from string import *

def def_subckt():
	subckt_flag=0

###########################################################################################################################

	for line_index in range(len(con.CODE_DATA)):
		
		LINE=con.CODE_DATA[line_index]
		scan_code_data=LINE.split()
		
		if scan_code_data==[]:
			continue
			
		
		for keyword_index in range(len(scan_code_data)):
			
			if con.is_number(scan_code_data[keyword_index]):
				scan_code_data[keyword_index]=eval(scan_code_data[keyword_index])

###########################################################################################################################
			
		if scan_code_data[0]=="!SUBCKT":
			
			if subckt_flag!=0:
				eh.display_error(LINE,line_index,20,circuit_flag)
				
			subckt_flag=1
			
			arg=scan_code_data[2:]
				
			if len(scan_code_data)<2:
				eh.display_error(LINE,line_index,35,0)
			
			if type(scan_code_data[1])!=str:
				eh.display_error(LINE,line_index,49,0)
				
			if len(arg)==0:
				eh.display_error(LINE,line_index,21,0)
				
			for word in arg:
				if type(word)!=int:
					eh.display_error(LINE,line_index,22,str(word))
				if word < 0:
					eh.display_error(LINE,line_index,22,str(word))
				
			subckt_file_name=scan_code_data[1]
			
			SUBCKT_FILE=open(con.PREPATH+"\SUBCIRCUITS_USER_DEFINED\\"+subckt_file_name+".txt","w")
			temp=scan_code_data[2:]
			for t in range(len(temp)):
				temp[t]=str(temp[t])
			temp=join(temp,"\t")
			SUBCKT_FILE.write(temp+"\n")

			continue

###########################################################################################################################
			
		if scan_code_data[0]=="!END_SUBCKT":
			if subckt_flag!=1:
				eh.display_error(LINE,line_index,23,0)
				
			SUBCKT_FILE.close()
			subckt_flag=0

			continue

###########################################################################################################################
			
		if scan_code_data[0]=="SUBCKT" or scan_code_data[0]=="!FIX_VOLTAGE" or scan_code_data[0]=="AND_2" or scan_code_data[0]=="OR_2" or scan_code_data[0]=="NAND_2" \
		or scan_code_data[0]=="NOR_2" or scan_code_data[0]=="XOR_2" or scan_code_data[0]=="XNOR_2" or scan_code_data[0]=="BUFFER" or scan_code_data[0]=="NOT" or scan_code_data[0]=="TRISTATE_BUFFER" or scan_code_data[0]=="ND":
			
			if subckt_flag==1:
				temp=scan_code_data
				for t in range(len(temp)):
					temp[t]=str(temp[t])
				temp=join(temp,"\t")
				SUBCKT_FILE.write(temp+"\n")
			
			continue
			
###########################################################################################################################