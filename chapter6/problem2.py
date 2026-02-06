mark1 = int(input("Enter mark1: "))
mark2 = int(input("Enter mark2: "))
mark3 = int(input("Enter mark3: "))
mark4 = int(input("Enter mark4: "))

#find percentage 
total_percentage = (mark1 + mark2 + mark3 + mark4) / 4

if ((total_percentage >= 40) and (marks1 >= 33) and (marks2 >= 33) and (marks3 >= 33) and (marks4 >= 33)):
    print("You have passed the exam.")
else:
    print("You have failed the exam.")