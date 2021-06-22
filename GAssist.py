from popAssist import *

def userAction(text):
    print(text)    
    return False
# True로 하면 응답메세지가 안나옴
# False로 하면 구글어시스턴트가 대답해줌
steam = create_conversation_stream()
ga = GAssistant(steam, local_device_handler=userAction)

def onStart():
    print(">>> Start recording...")

while True:
    ga.assist(onStart)
    
