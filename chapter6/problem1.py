a1 = int(input("enter number1 : "))
a2 = int(input("enter number2 : "))
a3 = int(input("enter number3 : "))
a4 = int(input("enter number4 : "))
if(a1 >= a2 and a1 >= a3 and a1 >= a4):
    print("number1 is the greatest")
elif(a2 >= a1 and a2 >= a3 and a2 >= a4):
    print("number2 is the greatest")
elif(a3 >= a1 and a3 >= a2 and a3 >= a4):
    print("number3 is the greatest")
else:
    print("number4 is the greatest")