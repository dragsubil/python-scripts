class Robot:
	def __init__(self,name=None):
		print("INITified!")
		self.name=name
	
	def say_hi(self):

		print("hi my name is {},{}".format(self.name,self.phrase))

if __name__=="__main__":
	x=Robot()
	x.name='marvin'
	x.phrase='bitches'
	
	y="marvin"
	x.say_hi()