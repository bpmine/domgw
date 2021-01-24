#!/usr/bin/python3

import requests;
import json;
import time;
import random;

with open("token.txt","r") as fp:
    token=fp.readline().strip()

try:
    assert token
except:
    print("token undifined. Please create a token.txt file with the hue token inside it.")
    exit(0)

class Light:
    hue=None;
    num=None;
    
    def __init__(self,hue,num):
        self.hue=hue;
        self.num=num;

    def on(self):
        self.hue.lSet(self.num,True);
        
    def off(self):
        self.hue.lSet(self.num,False);

class Hue:
    cred=None;
    
    def __init__(self,cred):
        self.cred=cred;
    
    def listAPs():
        lst=[];

        r=requests.get('https://discovery.meethue.com');
        if (r.status_code!=200):
            raise Exception("Impossible to get bridge list");

        js=r.json();
        if (len(js)<=0):
            raise Exception("Bridge list empty");

        for elm in js:
            bridge={'ip':elm['internalipaddress'],'id':elm['id']};
            lst.append(bridge);

        return lst;

    def bind(ip,name):
        obj={'devicetype':name};
        r=requests.post("http://%s/api" %(ip),data=json.dumps(obj));
        if (r.status_code!=200):
            raise Exception("Error get token request");

        js=r.json();
        print(js);
        js=js[0];
        if 'success' in js:
            if 'username' in js['success']:
                token=js['success']['username'];
                cred={'ip':ip,'token':token};    
                return Hue(cred);

        return None;

    def create(ip):
        return Hue({'ip':ip,'token':token});

    def getLights(self):
        lst=[];
        r=requests.get("http://%s/api/%s/lights" % (self.cred['ip'],self.cred['token']));
        if (r.status_code!=200):
            raise Exception("Error get list of lights request");

        js=r.json();
        for e in js.keys():
            nm=js[e]['name'];
            lst.append({'num':int(e),'name':nm.encode('UTF8')});

        return lst;

    def getLight(self,num):
        return Light(self,num);

    def lSet(self,num,val):
        dta={'on':val};
        r=requests.put("http://%s/api/%s/lights/%d/state" % (self.cred['ip'],self.cred['token'],num),data=json.dumps(dta));
        if (r.status_code!=200):
            raise Exception("Error set of light request");

def test_bpc_hue():
    lst=Hue.listAPs();
    ip=lst[0]['ip'];

    hue=Hue.create(ip);

    #cred={'token':token,'ip':ip};

    lst=hue.getLights();
    for l in lst:
        print(l);

    a=hue.getLight(7);
    a.on();
    a.off();



