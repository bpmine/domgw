#!/usr/bin/python3
import pika
import requests
import json
from bpchue import Hue
from libadge import BadgeReader


class HueGW:
    hue=None;

    lampes={}

    def __init__(self):
        lst=Hue.listAPs();
        ip=lst[0]['ip'];

        self.hue=Hue.create(ip);

        lst=self.hue.getLights();
        for l in lst:
            self.lampes[l['name'].decode("utf8").strip()]=self.hue.getLight(l['num']);

        print("Liste des lampes hue:")
        for k in self.lampes.keys():
            print("  - %s" % (k) )

    def set(self,name,on):
        if (name in self.lampes):
            if (on==True):
                self.lampes[name].on()
            else:
                self.lampes[name].off()
        else:
            print("Lampe %s non trouve" % (name) )
                


class RabbitGW:
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

    def sendChat(self,msg):
        dta={
            "typ":"chat",
            "dst":"all",
            "msg":msg
             }
        
        self.send(json.dumps(dta))

    def send(self,msg):
        self.ch.basic_publish(exchange="minetest",
                              routing_key=".minetest.server",
                              body=msg)

    def close(self):
        self.ch.close()
        self.conn.close()

    def intern_cb(self,ch, method, properties, body):
        key=method.routing_key
        msg=body.decode()
        if (self.callback!=None):
            self.callback(key,msg);

        self.ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def start(self,callback):
        self.callback=callback;
        self.ch.basic_consume(queue="minetest_gw", on_message_callback=self.intern_cb)

        self.ch.start_consuming()

IP_TOUR='192.168.1.42'

hue=HueGW();

def cb(key,msg):
    print("Message recu: %s: %s" % (key,msg))

    msg=json.loads(msg)

    if 'typ' in msg:
        typ=msg['typ']
        if typ=='chat':
            if 'msg' in msg:
                print("Chat> %s" % (msg['msg']))
                if msg['msg']=='hueon':
                    hue.set("bureau Paul",True)
                if msg['msg']=='hueoff':
                    hue.set("bureau Paul",False)
                    
        elif typ=='tour':
            if 'num_start' in msg and 'num_end' in msg and 'col' in msg:
                num_start=int(msg['num_start'])
                num_end=int(msg['num_end'])
                col=msg['col']
                print("  - Led tour %s->%s: Couleur %s" % (num_start,num_end,col))

                r = requests.post('http://%s/leds/set?start=%s&col=%s&end=%s' % (IP_TOUR,num_start,col,num_end))
                print(r.text);

        elif typ=='hue':
            if 'name' in msg and 'cmd' in msg:
                name=msg['name']
                cmd=msg['cmd']

                print("  - Hue %s: %s" % (name,cmd))
                if cmd=='on':
                    hue.set(name,True)
                else:
                    hue.set(name,False)

with open('credentials.txt','r') as json_file:
    data = json.load(json_file)

IP=data['ip']
LOGIN=data['login']
PASS=data['pass']

r=RabbitGW(IP,LOGIN,PASS)

def eventCard(rdr,card):
    print(card)
    rdr.setGreenLed(True)
    r.sendChat("Badge Présenté: %s" % (card))

    dta={
            "typ":"badge",
            "id":card
    }        
    r.send(json.dumps(dta))

    

#badgeReader=BadgeReader("COM3")
#badgeReader.addListener(eventCard)
#badgeReader.start()

r.start(cb)

        



