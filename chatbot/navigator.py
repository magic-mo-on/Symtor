import os
import subprocess
## https://github.com/rahul15197/Disease-Detection-based-on-Symptoms

nluServer="symtor"
actionSever="symtoractions"
os.chdir(r"symtor")
while True:
    print("""1:open command window \n2:heroku login \n3:container login \n4:Run local NLU server \n5:Run local Action server \n6:push NLU server \n7:push action server \n8:exit""")
    n=int(input("\nenter choice:"))  
    if n==1:
        os.chdir(r"../")
        os.system("start cmd")
        os.chdir(r"symtor")
    elif n==2:
        os.system("heroku login")
    elif n==3:
        os.system("heroku container:login")
    elif n==4:
        os.system("rasa shell --endpoints testendpoints.yml -p 5057")
    elif n==5:
        os.system("rasa run actions -p 5056")
    elif n==6:
        os.system("git add .")
        message=input("enter commit message: ")
        os.system("git commit -m \"{}\"".format(message))
        os.system("heroku container:push web -a "+nluServer)
        os.system("heroku container:release web -a "+nluServer)
    elif n==7:
        os.chdir(r"actions")
        os.system("git add .")
        message=input("enter commit message:")
        os.system("git commit -m \"{}\"".format(message))
        os.system("heroku container:push web -a "+actionSever)
        os.system("heroku container:release web -a "+actionSever)
        os.chdir(r"../")
    else:
        break
