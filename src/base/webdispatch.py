'''
from flask_socketio import SocketIO,Namespace
import eventlet
eventlet.monkey_patch()

class CustomNamespace(Namespace):

    def on_connect(self):
        print("连接..")
        
    def on_disconnect(self):
        print("关闭连接")
        
    def on_message(self, data):
        print('received message: ' + data['data'])
        self.emit("response", {'age': 18})
    
    def send(self,data):
         self.emit("response", {'age': 18})
         '''