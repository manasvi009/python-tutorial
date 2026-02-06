p1 = "Make a lot of Money"
p2 = "buy now"
p3 = "subscribe this channel"
p4 = "click this link"

message = input("Enter the message: ")

if ((p1 in message) or (p2 in message) or (p3 in message) or (p4 in message)):
    print("This is a spam message.")
else:
    print("This is not a spam message.")
