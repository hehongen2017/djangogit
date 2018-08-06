class Car():
	#一次模拟汽车的尝试
	def __init__(self,make,model,year):
		#初始化汽车的属性
		self.make = make
		self.model = model
		self.year = year
		self.odometer_reading=0
		
	def get_descriptive_name(self):
		#打印整洁的描述性信息
		long_name = str(self.year)+' '+self.make+' '+self.model
		print(long_name.title())
	
	def read_odometer(self):
		#读取公里数
		if self.odometer_reading == 0:
			print("Now the current still zero!")
		else:
			print("This car has "+str(self.odometer_reading)+\
			" miles on it")
	
	def update_odometer(self,mileage):
		#更新公里数
		if mileage >= self.odometer_reading:
			self.odometer_reading = mileage
		else:
			print("You can't roll back an odometer!")
	
	def increment_odometer(self,miles):
		self.odometer_reading+=miles
	



		
	
