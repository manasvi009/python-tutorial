#function is a block of code which only runs when it is called. we can pass data, known as parameters, into a function. A function can return data as a result.
#functions are reusable pieces of code. they allow us to write code once and use it many times. they also help us to break our program into smaller and modular chunks.
#functions are defined using the def keyword, followed by the function name and parentheses. the code block within every function starts with a colon (:) and is indented.
#functions can take parameters, which are values that we can pass to the function when we call it. these parameters can be used within the function to perform operations or calculations. functions can also return values, which are the results of the operations performed within the function. we can use the return statement to specify what value a function should return.
#functions can be called by using their name followed by parentheses. if the function takes parameters, we can pass the required arguments within the parentheses when calling the function. functions can be called multiple times in a program, allowing us to reuse code and perform the same operations with different inputs.
#function defination 
def avg():
    num1 = int(input("Enter first number : "))
    num2 = int(input("Enter second number : "))
    num3 = int(input("Enter third number : "))
    average = (num1 + num2 + num3) / 3
    print(f"Average of {num1} , {num2} and {num3} is {average}")
  

#function call
avg()
print("Thnak you for using this program")
avg()
print("Thnak you for using this program")
