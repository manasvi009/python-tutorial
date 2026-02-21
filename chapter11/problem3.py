class Employee:
  salary = 7890
  increment = 20

  @property
  def salaryIncrement(self):
    return(self.salary + self.salary * (self.increment/100))


  @salaryIncrement.setter
  def salaryIncrement(self , salary):
    self.increment = ((salary/self.salary)-1)*100 

e = Employee()
print(e.salaryIncrement)
e.salaryIncrement = 180
print(e.increment)
