import sys
import subprocess

def main():
	try:
		import matplotlib.pyplot
		import serial
	except:
		print "Packages matplotlib and pyserial are not installed in your system."
		print "Commands requiring these packages will not work.\n"
		agree=raw_input(str("Do you want to install the packages now?? (y/n) : "))
		if agree=="y":
			subprocess.check_call([sys.executable, '-m', 'pip', 'install','matplotlib','--user'])
			subprocess.check_call([sys.executable, '-m', 'pip', 'install','pyserial','--user'])
			
			print "\n"
			exit()
		
		elif agree=="n":
			import simulator
		
		else:
			print "Process ended."
			exit()
	else:
		import simulator
	
	
if __name__ =='__main__':
	main()