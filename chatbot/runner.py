import requests
#url = 'https://symtor.herokuapp.com/webhooks/rest/webhook'
url = 'http://localhost:5005/webhooks/rest/webhook'
myobj = {
"message": "hi",
"sender": 1,
}
sender=input("please enter sender name:")
myobj["sender"]=sender
while(True):
    message=input("user->")
    if(message=="quit"):
        break
    myobj["message"]=message
    x = requests.post(url, json = myobj)
    # print(type(x))
    x=x.json()
    print(x[0])
    # if action
    # for i in range(len(x)):
    #     if "text" in x[i]:
    #         print("bot->",x[i]['text'])
    #     else:
    #         print("bot->",x[i]['image'])