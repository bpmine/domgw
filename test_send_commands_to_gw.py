import pika
import requests
import json
import time;



class RabbitCmds:
    ip=None
    login=None
    passe=None

    conn=None
    ch=None

    def connect(self):
        credentials = pika.PlainCredentials(self.login, self.passe)

        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip,
                                      5672,
                                      '/',
                                      credentials)
            )
        self.ch = self.conn.channel()
        
    
    def __init__(self,ip,login,passe):
        self.ip=ip
        self.login=login
        self.passe=passe

        self.connect()

    def send(self,obj):
        self.ch.basic_publish(exchange="minetest",
                              routing_key=".minetest.gw",
                              body=json.dumps(obj))

    def close(self):
        self.ch.close()
        self.conn.close()

    

r=RabbitCmds('35.180.75.216','minetest_server','minetest38')

cmd={"typ":"hue","name":"bureau Paul","cmd":"on"}
r.send(cmd);
time.sleep(2)
cmd={"typ":"hue","name":"bureau Paul","cmd":"off"}
r.send(cmd);


r.close()
    
