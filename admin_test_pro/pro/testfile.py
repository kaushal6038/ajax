import datetime
seconds = datetime.datetime.now()
print(seconds.minute)

import time
time.sleep(4)

# with open("/checkfile.txt", "w") as f:
#     f.write("Hello World form") 

file = open("checkfile.txt", "a") 
file.write("Your text goes here "+ str(seconds)) 
file.close() 
