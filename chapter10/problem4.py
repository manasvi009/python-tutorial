class calculater:

    def __init__(self , number):
        self.number = number

    def square(self):
       print(f"square is : {self.number*self.number}")
    def cube(self):
       print(f"cube is : {self.number*self.number*self.number}")
    def squareroot(self):
       print(f"squareroot is : {self.number**1/2}")


    @staticmethod
    def hello():
            print("Hello world")
   


a= calculater(4)
a.square()
a.cube()
a.squareroot()