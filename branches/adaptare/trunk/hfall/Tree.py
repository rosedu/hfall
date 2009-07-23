"""
Tree Class
"""

__version__ = '0.1'
__authors__ =   'Mihai Maruseac (mihai.maruseac@gmail.com)' ,\
                'Laura-Mihaela Vasilescu (vasilescu.laura@gmail.com)'

class Tree():

	def __init__(self, value, sons):
		self.value = value
		self.sons = sons
		
	def add_son(self, son):
		self.sons.append(son)
		
	def print_sons(self):
		print self.sons
		
	def aux_print(self, NT):
	    string = "%s: " % self.value.__str__() + "\n"
	    aux = NT
	    NT += 1
	    for son in self.sons:
	        string = string + NT*"\t" + son.aux_print(NT)
	    NT = aux
	    return string	    
	
	def __str__(self):
	    return self.aux_print(0)
