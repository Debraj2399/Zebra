def BUFFER(a):
	return (a)

def TRISTATE_BUFFER(a,b,c):
	return (NOT(a)&c)|(a&b)

def AND_2(a,b):
	return (a&b)
	
def OR_2(a,b):
	return (a|b)

def NOT(a):
	return (1-a)
	
def NAND_2(a,b):
	return NOT(a&b)
	
def NOR_2(a,b):
	return NOT(a|b)

def XOR_2(a,b):
	return (a^b)
	
def XNOR_2(a,b):
	return not(a^b)
