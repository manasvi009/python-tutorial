def myfunc():
    print("Hello Manasvi")

myfunc()
print(__name__)

if __name__ == "__main__":
    #if this code is directly executed by running the file its present in
    print("We are directly running this code")
    myfunc()
    print(__name__)