class programmer:
    company = "Microsoft"

    def __init__(self, name , salary , pincode):
        self.name = name
        self.salary = salary
        self.pincode = pincode
        
p=programmer("Manasvi" , 1200000 , 395006)
print(p.company , p.name ,p.salary , p.pincode)

