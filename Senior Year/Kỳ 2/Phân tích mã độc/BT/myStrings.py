import string, sys

fname = input("Enter filename: ")
if len(fname) == 0:
    print ('Pls enter a file name')
    sys.exit()
    
fstring = ""
min = 4

with open(fname, errors="ignore") as f:  # Python 3.x
#with open(fname, "rb") as f:           # Python 2.x
    result = ""
    for c in f.read():
        if c in string.printable:
            result += c
            continue
        if len(result) >= min:
            fstring += result+'\n'
        result = ""
    print(fstring)      
