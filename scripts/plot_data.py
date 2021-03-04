import config as con
import time
from string import *
try:
	import matplotlib.pyplot as plt
	import numpy as np
	import turtle
except:
	con.PLOT_ALLOW_FLAG=0
else:
	con.PLOT_ALLOW_FLAG=1

def plot_nodes():
	con.PLOT_DATA=np.array(con.PLOT_DATA).T
	for data_column_index in range(len(con.PLOT_NODE)):
		plt.yticks([])
		plt.plot(con.PLOT_DATA[0],(con.PLOT_DATA[data_column_index+1]-data_column_index*2.0),label=str(con.PLOT_NODE[data_column_index]))
		plt.legend(fontsize=8,loc=1)
	plt.show()


def animate_plot_nodes_setup():
	
	COLOR=["black","red","orange","yellow","green","blue","indigo","violet"]
	con.screen=turtle.Screen()
	con.initial_x=-300
	con.y_div=600.0/(len(con.PLOT_NODE)+1)
	con.initial_y=300-con.y_div
	
	con.screen.setup(600,600,startx=766,starty=0)
	con.screen.tracer(0)
	
	textTurtle=turtle.Turtle()
	textTurtle.speed(0)
	textTurtle.ht()
	textTurtle.width(2)
	
	for count_plot in range(len(con.PLOT_NODE)):
		textTurtle.pu()
		textTurtle.goto(250,280-(count_plot)*10)
		textTurtle.pd()
		
		textTurtle.color("black")
		textTurtle.write(str(con.PLOT_NODE[count_plot]))
		
		textTurtle.pu()
		textTurtle.goto(260,287-(count_plot)*10)
		textTurtle.pd()
		
		textTurtle.color(COLOR[count_plot%8])
		textTurtle.fd(20)
		
		con.TURTLES.append(turtle.Turtle())
		con.TURTLES[count_plot].speed(0)
		con.TURTLES[count_plot].color(COLOR[count_plot%8])
		con.TURTLES[count_plot].width(2)
		con.TURTLES[count_plot].ht()
		con.TURTLES[count_plot].pu()
		con.TURTLES[count_plot].setpos(con.initial_x,con.initial_y-(count_plot*con.y_div))
		con.TURTLES[count_plot].pd()
		
		
def animate_plot_nodes(pl):
	for count_plot in range(len(con.PLOT_NODE)):
		con.TURTLES[count_plot].goto(con.initial_x+pl[0]*50,con.initial_y-(count_plot*con.y_div)+(pl[count_plot+1]*(con.y_div/2.0)))
	if (con.initial_x+pl[0]*50)>=300:
		con.initial_x-=600
		for count_plot in range(len(con.PLOT_NODE)):
			con.TURTLES[count_plot].clear()
			con.TURTLES[count_plot].pu()
			con.TURTLES[count_plot].setpos(con.initial_x,con.initial_y-(count_plot*con.y_div))
			con.TURTLES[count_plot].pd()
		
	con.screen.update()
	
###########################################################################################################################

def real_time_print_setup():
	con.screen_rt=turtle.Screen()
	con.turtle_write=turtle.Turtle()
	con.turtle_write_head=turtle.Turtle()
	
	con.temp_height=((((len(con.PRINT_NODE)/10)+1)*2)+((len(con.PRINT_NODE)/10)-1))*16

	con.screen_rt.setup(700,con.temp_height+100,startx=666,starty=0)
	con.screen_rt.bgcolor("black")
	con.screen_rt.tracer(0,0)
	
	con.turtle_write.speed(0)
	con.turtle_write.ht()
	con.turtle_write.clear()
	con.turtle_write.color("white")
	
	con.turtle_write_head.speed(0)
	con.turtle_write_head.ht()
	con.turtle_write_head.clear()
	con.turtle_write_head.pu()
	con.turtle_write_head.goto(0,(con.temp_height/2)+20)
	con.turtle_write_head.pd()
	con.turtle_write_head.color("white")
	
	heading="######################## THIS IS REAL TIME PRINTING ########################"
	con.turtle_write_head.write(heading,move=False,align="center",font=("Courier New",10,"bold"))
	
	for print_node_index in range(len(con.PRINT_NODE)):
		if con.PRINT_NODE[print_node_index]=='time':
			con.PRINT_NODE[print_node_index]='t(s)'
		else:
			con.PRINT_NODE[print_node_index]=str(con.PRINT_NODE[print_node_index])
	

def real_time_print():
	con.turtle_write.clear()
	
	con.turtle_write.goto(0,-(15+(con.temp_height/2)))
	temp_print=""
	print_total=""
	
	for print_node_index in range(len(con.PRINT_NODE_INDEX)):
		if con.PRINT_NODE_INDEX[print_node_index]!='time':
			temp_print=temp_print+str(int(con.NODE_DATA[con.PRINT_NODE_INDEX[print_node_index]][-1]))+"\t"
		else:
			temp_print=temp_print+str(round((time.clock()-con.start_time),2))+"\t"

		if (print_node_index+1)%10==0:
			index=print_node_index/10

			temp_print=temp_print[:-1]
			
			con.temp_print_node=join((con.PRINT_NODE[(index*10):((index+1)*10)]),'\t')
			
			print_total=print_total+con.temp_print_node+"\n"+temp_print+"\n\n"
			
			temp_print=""
		
			
	if (len(con.PRINT_NODE))%10!=0:
		temp_print=temp_print[:-1]
		con.temp_print_node=join((con.PRINT_NODE[((len(con.PRINT_NODE)/10)*10):len(con.PRINT_NODE)]),'\t')
		print_total=print_total+con.temp_print_node+"\n"+temp_print
		
	con.turtle_write.write(print_total,move=False,align="center",font=("Courier New",10,"bold"))
	con.screen_rt.update()
	
	